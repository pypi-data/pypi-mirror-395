import imaplib
import smtplib
import email
from email.header import decode_header
import time
import os
from email import policy
from email.message import EmailMessage
import mimetypes

from exchangelib import Credentials, HTMLBody, Message, Mailbox
#from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
from exchangelib import OAuth2Credentials, Identity, Configuration, Account, DELEGATE
import requests
import base64
from bs4 import BeautifulSoup


##### please uncomment this line to ignore certificate checking (owa)
#BaseProtocol.HTTP_ADAPTER_CLS=NoVerifyHTTPAdapter

from msal import ConfidentialClientApplication
from oauthlib.oauth2 import OAuth2Token

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.utils import MetManagement
    from Orange.widgets.orangecontrib.IO4IT.utils import keys_manager
else:
    from orangecontrib.AAIT.utils import MetManagement
    from orangecontrib.IO4IT.utils import keys_manager


def clean_addresses(field,myemail):
    """Retourne une liste d'adresses nettoyées sans ton adresse"""
    if not field:
        return []
    addresses = email.utils.getaddresses([field])
    return [addr for name, addr in addresses if addr.lower() != myemail.lower()]

def mail_in_folder(agent_name, type="in"):
    if agent_name is None or agent_name == "":
        print("agent_name doit etre renseigné")
        return None
    chemin_dossier= MetManagement.get_path_mailFolder()
    if type == "in":
        if not os.path.exists(chemin_dossier):
            os.makedirs(chemin_dossier)
        real_time = MetManagement.get_second_from_1970()
        folder_in = chemin_dossier + "/" + str(agent_name) + "/in/" + str(real_time)
        folder_out = chemin_dossier + "/" + str(agent_name) + "/out/" + str(real_time)
        if not os.path.exists(folder_in) and not os.path.exists(folder_out):
            os.makedirs(folder_in)
            os.makedirs(folder_out)
        else:
            time.sleep(1.5)
            mail_in_folder(agent_name, "in")
        return folder_in
    if  type == "out":
        return chemin_dossier + str(agent_name) + "/in/", chemin_dossier + "/" + str(agent_name) + "/out/"


def check_new_emails(offusc_conf_agent,type_co, list_agent_email=[]):
    if type_co=="IMAP4_SSL":
        try:
            agent,my_domain,password,interl_seconds,alias=keys_manager.lire_config_imap4_ssl(offusc_conf_agent)
            myemail=agent + my_domain
            imap = imaplib.IMAP4_SSL("imap.gmail.com")
            imap.login(myemail, password)
            imap.select("inbox")
            status, messages = imap.search(None, 'UNSEEN')
            mail_ids = messages[0].split()
            if not mail_ids:
                print("Aucun nouveau mail.")
            else:
                for mail_id in mail_ids:
                    if list_agent_email != []:
                        white_list, black_list = keys_manager.lire_list_email(list_agent_email)
                    else:
                        white_list=[]
                        black_list=[]
                    time.sleep(1.5)
                    output_lines = []
                    _, msg_data = imap.fetch(mail_id, '(BODY.PEEK[])')
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            from email.parser import BytesParser

                            # Utilise :
                            msg = BytesParser(policy=policy.default).parsebytes(response_part[1])

                            # Sujet
                            subject, encoding = decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding if encoding else "utf-8")

                            # Expéditeur
                            from_ = msg.get("From")
                            # Destinataires
                            to_emails = clean_addresses(msg.get("To", ""),myemail)
                            cc_emails = clean_addresses(msg.get("Cc", ""),myemail)
                            if (to_emails != [] or cc_emails != []) and alias == "":
                                if myemail not in to_emails or myemail not in cc_emails:
                                    print(f"l'adresse de reception est un alias : {to_emails}")
                                    continue
                            if (to_emails == [] and cc_emails == []) and alias != "":
                                print(f"l'adresse de reception est un alias : {alias}")
                                continue
                            ## passe en lu si ce n'est pas un alias
                            imap.store(mail_id, '+FLAGS', '\\Seen')
                            # Corps
                            body = ""
                            if msg.is_multipart():
                                for part in msg.walk():
                                    content_type = part.get_content_type()
                                    content_disposition = str(part.get("Content-Disposition"))

                                    if content_type == "text/plain" and "attachment" not in content_disposition:
                                        payload = part.get_payload(decode=True)
                                        charset = part.get_content_charset()
                                        body = payload.decode(charset if charset else "utf-8", errors="replace")
                                        break
                                    elif content_type == "text/html" and "attachment" not in content_disposition:
                                        html_body = part.get_content()
                                        soup = BeautifulSoup(html_body, "html.parser")

                                        # Remove signatures or footers by rule
                                        for block in soup.find_all(["footer", "style", "script"]):
                                            block.decompose()

                                        body = soup.get_text(separator="\n", strip=True)


                            else:
                                body = msg.get_payload(decode=True).decode(errors="replace")
                            if alias != "":
                                agent = alias


                            folder = mail_in_folder(agent, "in")
                            if folder is None:
                                print("erreur dans le folder de mail")
                                return
                            ignored_pj=""
                            for part in msg.iter_attachments():
                                filename = part.get_filename()
                                if filename:
                                    if len(filename)<5:
                                        continue
                                    if not (filename.endswith(".pdf") or filename.endswith(".docx")):
                                        if ignored_pj!="":
                                            ignored_pj+=";"
                                        ignored_pj+=filename
                                        continue  # Fichier ignoré

                                    folder_pj = folder + "/" + "pj"
                                    if not os.path.exists(folder_pj):
                                        os.makedirs(folder_pj)
                                    filepath = os.path.join(folder_pj, filename)
                                    with open(filepath, "wb") as f:
                                        f.write(part.get_payload(decode=True))
                                    f.close()

                            # Format de sortie
                            output_lines.append(f"#$who : {myemail}")
                            output_lines.append(f"#$eme : {from_}")
                            output_lines.append(f"#$des : {', '.join(to_emails)}")
                            output_lines.append(f"#$cop : {', '.join(cc_emails)}")
                            output_lines.append("#$pri : Normale")
                            output_lines.append(f"#$tit : {subject}")
                            output_lines.append(f"#$ipj : {ignored_pj}")
                            output_lines.append(f"#$txt : {body.strip()}")
                            output_lines.append("")
                            print("----------------------------------------")
                            print(f"mail recu de {from_}")
                            print("----------------------------------------")
                            if white_list != [] and from_ not in white_list:
                                print("cette adresse n'est pas dans la white list")
                                continue
                            if black_list != [] and from_ in black_list:
                                print("cette adresse est dans la black list")
                                continue
                            if output_lines != []:
                                with open(folder + "/" + "mail.txt", "w", encoding="utf-8") as f:
                                    f.write("\n".join(output_lines))
                                    f.close()

                                with open(folder + "/" + "mail.ok", "w") as f:
                                    f.close()



            imap.logout()
        except Exception as e:
            print(f"Erreur lors de la vérification des mails : {e}")
    elif type_co=="MICROSOFT_EXCHANGE_OWA":
        try:
            mail, alias, server, username, password, interval_second = keys_manager.lire_config_owa(
                offusc_conf_agent)
            credentials = Credentials(username=username, password=password)
            config = Configuration(
                server=server,
                credentials=credentials,
            )

            account = Account(
                primary_smtp_address=alias,
                credentials=credentials,
                config=config,
                autodiscover=False,
                access_type=DELEGATE
            )

            # Inbox
            inbox = account.inbox.filter(is_read=False)


            if not inbox:
                print("Aucun nouveau mail.")
            else:
                for item in inbox.order_by('datetime_received'):
                    if list_agent_email != []:
                        white_list, black_list = keys_manager.lire_list_email(list_agent_email)
                    else:
                        white_list, black_list = [], []
                    if not isinstance(item,Message):
                        print('mail non standard (reunion etc...), ignore')
                        continue
                    time.sleep(1.5)
                    output_lines = []

                    from_ = item.sender.email_address
                    subject = item.subject or "(Sans sujet)"
                    to_emails = [rec.email_address for rec in item.to_recipients or []]
                    cc_emails = [rec.email_address for rec in item.cc_recipients or []]

                    if (to_emails or cc_emails) and alias == "":
                        if mail not in to_emails and mail not in cc_emails:
                            print(f"L'adresse de réception est un alias : {to_emails}")
                            continue
                    if not to_emails and not cc_emails and alias != "":
                        print(f"L'adresse de réception est un alias : {alias}")
                        continue

                    # Marquer comme lu
                    item.is_read = True
                    item.save()

                    # Corps du mail
                    body = ""
                    if item.body.body_type == "HTML":
                        soup = BeautifulSoup(item.body, "html.parser")
                        for block in soup.find_all(["footer", "style", "script"]):
                            block.decompose()
                        body = soup.get_text(separator="\n", strip=True)
                    else:
                        body = item.body.strip()

                    if alias != "":
                        agent = alias

                    folder = mail_in_folder(agent, "in")
                    if folder is None:
                        print("Erreur dans le folder de mail")
                        continue

                    ignored_pj = ""
                    for attachment in item.attachments:
                        if not hasattr(attachment, 'name') or len(attachment.name) < 5:
                            continue
                        if not (attachment.name.endswith(".pdf") or attachment.name.endswith(".docx")):
                            if ignored_pj:
                                ignored_pj += ";"
                            ignored_pj += attachment.name
                            continue

                        folder_pj = os.path.join(folder, "pj")
                        os.makedirs(folder_pj, exist_ok=True)
                        filepath = os.path.join(folder_pj, attachment.name)
                        with open(filepath, "wb") as f:
                            f.write(attachment.content)

                    # Format sortie
                    output_lines.append(f"#$who : {mail}")
                    output_lines.append(f"#$eme : {from_}")
                    output_lines.append(f"#$des : {', '.join(to_emails)}")
                    output_lines.append(f"#$cop : {', '.join(cc_emails)}")
                    output_lines.append("#$pri : Normale")
                    output_lines.append(f"#$tit : {subject}")
                    output_lines.append(f"#$ipj : {ignored_pj}")
                    output_lines.append(f"#$txt : {body.strip()}")
                    output_lines.append("")

                    print("----------------------------------------")
                    print(f"Mail reçu de {from_}")
                    print("----------------------------------------")

                    if white_list and from_ not in white_list:
                        print("Cette adresse n'est pas dans la white list")
                        continue
                    if black_list and from_ in black_list:
                        print("Cette adresse est dans la black list")
                        continue

                    with open(os.path.join(folder, "mail.txt"), "w", encoding="utf-8") as f:
                        f.write("\n".join(output_lines))
                    with open(os.path.join(folder, "mail.ok"), "w") as f:
                        pass

        except Exception as e:
            print(f"Erreur lors du traitement du mail : {e}")
    elif type_co == "MICROSOFT_EXCHANGE_OAUTH2":
        try:
            client_id, client_secret, tenant_id, user_email= keys_manager.lire_config_oauth2(
                offusc_conf_agent)
            authority = f"https://login.microsoftonline.com/{tenant_id}"

            app = ConfidentialClientApplication(
                client_id=client_id,
                client_credential=client_secret,
                authority=authority
            )

            token_result = app.acquire_token_for_client(scopes=["https://outlook.office365.com/.default"])
            if "access_token" not in token_result:
                raise Exception("Impossible d'obtenir un token : ", token_result.get("error_description"))

            token_for_exchangelib = OAuth2Token({
                'access_token': token_result['access_token'],
                'expires_in': token_result.get('expires_in', 3600),
                'token_type': token_result.get('token_type', 'Bearer'),
                'scope': 'https://outlook.office365.com/.default'
            })

            credentials = OAuth2Credentials(
                client_id=client_id,
                client_secret=client_secret,
                tenant_id=tenant_id,
                identity=Identity(primary_smtp_address=user_email),
                access_token=token_for_exchangelib
            )

            config = Configuration(
                credentials=credentials,
                auth_type='OAuth 2.0',
                service_endpoint='https://outlook.office365.com/EWS/Exchange.asmx'
            )

            account = Account(
                primary_smtp_address=user_email,
                config=config,
                autodiscover=True,
                access_type=DELEGATE
            )

            inbox = account.inbox.filter(is_read=False)

            if not inbox:
                print("Aucun nouveau mail.")
            else:
                for item in inbox.order_by('datetime_received'):
                    if list_agent_email:
                        white_list, black_list = keys_manager.lire_list_email(list_agent_email)
                    else:
                        white_list, black_list = [], []

                    if not isinstance(item, Message):
                        print('mail non standard (reunion etc...), ignore')
                        continue

                    from_ = item.sender.email_address
                    subject = item.subject or "(Sans sujet)"
                    to_emails = [rec.email_address for rec in item.to_recipients or []]
                    cc_emails = [rec.email_address for rec in item.cc_recipients or []]

                    # Marquer comme lu
                    item.is_read = True
                    item.save()

                    if item.body.body_type == "HTML":
                        soup = BeautifulSoup(item.body, "html.parser")
                        for block in soup.find_all(["footer", "style", "script"]):
                            block.decompose()
                        body = soup.get_text(separator="\n", strip=True)
                    else:
                        body = item.body.strip()

                    folder = mail_in_folder(user_email, "in")
                    if folder is None:
                        print("Erreur dans le folder de mail")
                        continue

                    ignored_pj = ""
                    for attachment in item.attachments:
                        if not hasattr(attachment, 'name') or len(attachment.name) < 5:
                            continue
                        if not (attachment.name.endswith(".pdf") or attachment.name.endswith(".docx")):
                            ignored_pj += (";" if ignored_pj else "") + attachment.name
                            continue

                        folder_pj = os.path.join(folder, "pj")
                        os.makedirs(folder_pj, exist_ok=True)
                        filepath = os.path.join(folder_pj, attachment.name)
                        with open(filepath, "wb") as f:
                            f.write(attachment.content)

                    output_lines = [
                        f"#$who : {user_email}",
                        f"#$eme : {from_}",
                        f"#$des : {', '.join(to_emails)}",
                        f"#$cop : {', '.join(cc_emails)}",
                        "#$pri : Normale",
                        f"#$tit : {subject}",
                        f"#$ipj : {ignored_pj}",
                        f"#$txt : {body.strip()}",
                        ""
                    ]

                    print("----------------------------------------")
                    print(f"Mail reçu de {from_}")
                    print("----------------------------------------")

                    if white_list and from_ not in white_list:
                        print("Cette adresse n'est pas dans la white list")
                        continue
                    if black_list and from_ in black_list:
                        print("Cette adresse est dans la black list")
                        continue

                    with open(os.path.join(folder, "mail.txt"), "w", encoding="utf-8") as f:
                        f.write("\n".join(output_lines))
                    with open(os.path.join(folder, "mail.ok"), "w") as f:
                        pass
        except Exception as e:
            print(f"Erreur OAuth2 lors du traitement du mail : {e}")

    elif type_co == "MICROSOFT_EXCHANGE_OAUTH2_MICROSOFT_GRAPH":
        try:
            print("🔍 [DEBUG] Début de la vérification des emails avec Microsoft Graph OAuth2")
            client_id, client_secret, tenant_id, user_email = keys_manager.lire_config_oauth2(
                offusc_conf_agent)
            print(f"🔍 [DEBUG] Configuration lue - User: {user_email}, Tenant: {tenant_id}")

            authority = f"https://login.microsoftonline.com/{tenant_id}"

            app = ConfidentialClientApplication(
                client_id=client_id,
                client_credential=client_secret,
                authority=authority
            )
            print("🔍 [DEBUG] Application MSAL créée")

            # Essayer d'abord avec les permissions d'application (Client Credentials)
            token_result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
            if "access_token" not in token_result:
                raise Exception("Impossible d'obtenir un token : ", token_result.get("error_description"))

            print("🔍 [DEBUG] Token d'accès obtenu avec succès (Client Credentials)")
            access_token = token_result['access_token']
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            # Récupérer les emails non lus
            graph_url = f"https://graph.microsoft.com/v1.0/users/{user_email}/messages"
            params = {
                '$filter': 'isRead eq false',
                '$orderby': 'receivedDateTime asc',
                '$select': 'id,subject,sender,toRecipients,ccRecipients,receivedDateTime,body,hasAttachments'
            }

            print(f"🔍 [DEBUG] Requête Graph API: {graph_url}")
            print(f"🔍 [DEBUG] Paramètres: {params}")

            try:
                response = requests.get(graph_url, headers=headers, params=params)
                response.raise_for_status()
                emails_data = response.json()
                print(
                    f"🔍 [DEBUG] Réponse Graph API reçue - Nombre d'emails non lus: {len(emails_data.get('value', []))}")
            except requests.exceptions.HTTPError as e:
                if response.status_code == 403:
                    print("🔍 [DEBUG] Erreur 403 - Permissions insuffisantes")
                    print("🔍 [DEBUG] ==============================================")
                    print("🔍 [DEBUG] ACTION REQUISE - Contactez votre IT Admin:")
                    print("🔍 [DEBUG] ==============================================")
                    print("🔍 [DEBUG] Votre application Azure AD manque des permissions.")
                    print("🔍 [DEBUG] App: IA-ODATAMINING")
                    print("🔍 [DEBUG] ID: 30ae55f5-f41e-4d44-afcc-082e4b803ba1")
                    print("🔍 [DEBUG] Tenant: 9988c2b8-3feb-4426-aeb7-b8d695bcd025")
                    print("🔍 [DEBUG] ")
                    print("🔍 [DEBUG] Permissions manquantes (Application type):")
                    print("🔍 [DEBUG] - Mail.Read - pour lire les emails")
                    print("🔍 [DEBUG] - Mail.Send - pour envoyer des emails")
                    print("🔍 [DEBUG] ")
                    print("🔍 [DEBUG] INFORMATIONS POUR VOTRE IT ADMIN:")
                    print("🔍 [DEBUG] 1. Azure Portal → Azure AD → App registrations")
                    print("🔍 [DEBUG] 2. Trouver l'app: IA-ODATAMINING")
                    print("🔍 [DEBUG] 3. API permissions → Add permission → Microsoft Graph")
                    print("🔍 [DEBUG] 4. Application permissions → Mail.Read + Mail.Send")
                    print("🔍 [DEBUG] 5. Grant admin consent")
                    print("🔍 [DEBUG] ")
                    print("🔍 [DEBUG] URL de consentement admin:")
                    print(f"🔍 [DEBUG] https://login.microsoftonline.com/{tenant_id}/adminconsent?client_id={client_id}")
                    print("🔍 [DEBUG] ==============================================")
                    raise Exception(
                        "❌ Permissions insuffisantes. Contactez votre IT Admin pour ajouter Mail.Read et Mail.Send permissions à l'application IA-ODATAMINING.")
                else:
                    raise e
            if not emails_data.get('value'):
                print("Aucun nouveau mail.")
            else:
                for i, email_item in enumerate(emails_data['value']):
                    print(f"🔍 [DEBUG] Traitement de l'email {i + 1}/{len(emails_data['value'])}")
                    if list_agent_email:
                        white_list, black_list = keys_manager.lire_list_email(list_agent_email)
                        print(f"🔍 [DEBUG] Listes chargées - White: {len(white_list)}, Black: {len(black_list)}")
                    else:
                        white_list, black_list = [], []

                    time.sleep(1.5)
                    output_lines = []

                    email_id = email_item['id']
                    from_ = email_item['sender']['emailAddress']['address']
                    subject = email_item.get('subject', '(Sans sujet)')
                    to_emails = [rec['emailAddress']['address'] for rec in email_item.get('toRecipients', [])]
                    cc_emails = [rec['emailAddress']['address'] for rec in email_item.get('ccRecipients', [])]

                    print(f"🔍 [DEBUG] Email ID: {email_id}")
                    print(f"🔍 [DEBUG] De: {from_}, Sujet: {subject}")
                    print(f"🔍 [DEBUG] Destinataires: {to_emails}, CC: {cc_emails}")

                    # Marquer comme lu
                    mark_read_url = f"https://graph.microsoft.com/v1.0/users/{user_email}/messages/{email_id}"
                    patch_data = {'isRead': True}
                    print(f"🔍 [DEBUG] Marquage comme lu: {mark_read_url}")
                    requests.patch(mark_read_url, headers=headers, json=patch_data)

                    # Récupérer le corps du message
                    body = ""
                    if email_item.get('body'):
                        body_content = email_item['body'].get('content', '')
                        if email_item['body'].get('contentType') == 'html':
                            print("🔍 [DEBUG] Corps HTML détecté, nettoyage en cours")
                            soup = BeautifulSoup(body_content, "html.parser")
                            for block in soup.find_all(["footer", "style", "script"]):
                                block.decompose()
                            body = soup.get_text(separator="\n", strip=True)
                        else:
                            body = body_content.strip()
                    print(f"🔍 [DEBUG] Corps du message extrait (longueur: {len(body)})")

                    folder = mail_in_folder(user_email, "in")
                    if folder is None:
                        print("Erreur dans le folder de mail")
                        continue
                    print(f"🔍 [DEBUG] Dossier de mail: {folder}")

                    ignored_pj = ""
                    # Traiter les pièces jointes si elles existent
                    if email_item.get('hasAttachments'):
                        print("🔍 [DEBUG] Pièces jointes détectées, récupération en cours")
                        attachments_url = f"https://graph.microsoft.com/v1.0/users/{user_email}/messages/{email_id}/attachments"
                        att_response = requests.get(attachments_url, headers=headers)
                        att_response.raise_for_status()
                        attachments_data = att_response.json()

                        print(f"🔍 [DEBUG] {len(attachments_data.get('value', []))} pièce(s) jointe(s) trouvée(s)")
                        for attachment in attachments_data.get('value', []):
                            attachment_name = attachment.get('name', '')
                            print(f"🔍 [DEBUG] Pièce jointe: {attachment_name}")
                            if len(attachment_name) < 5:
                                continue
                            if not (attachment_name.endswith(".pdf") or attachment_name.endswith(".docx")):
                                ignored_pj += (";" if ignored_pj else "") + attachment_name
                                print(f"🔍 [DEBUG] Pièce jointe ignorée: {attachment_name}")
                                continue

                            folder_pj = os.path.join(folder, "pj")
                            os.makedirs(folder_pj, exist_ok=True)
                            filepath = os.path.join(folder_pj, attachment_name)

                            # Décoder le contenu base64
                            content_bytes = base64.b64decode(attachment.get('contentBytes', ''))
                            with open(filepath, "wb") as f:
                                f.write(content_bytes)
                            print(f"🔍 [DEBUG] Pièce jointe sauvegardée: {filepath}")

                    # Format sortie
                    output_lines = [
                        f"#$who : {user_email}",
                        f"#$eme : {from_}",
                        f"#$des : {', '.join(to_emails)}",
                        f"#$cop : {', '.join(cc_emails)}",
                        "#$pri : Normale",
                        f"#$tit : {subject}",
                        f"#$ipj : {ignored_pj}",
                        f"#$txt : {body.strip()}",
                        ""
                    ]

                    print("----------------------------------------")
                    print(f"Mail reçu de {from_}")
                    print("----------------------------------------")

                    if white_list and from_ not in white_list:
                        print("Cette adresse n'est pas dans la white list")
                        continue
                    if black_list and from_ in black_list:
                        print("Cette adresse est dans la black list")
                        continue

                    mail_txt_path = os.path.join(folder, "mail.txt")
                    mail_ok_path = os.path.join(folder, "mail.ok")
                    print(f"🔍 [DEBUG] Sauvegarde du mail: {mail_txt_path}")
                    with open(mail_txt_path, "w", encoding="utf-8") as f:
                        f.write("\n".join(output_lines))
                    with open(mail_ok_path, "w") as f:
                        pass
                    print("🔍 [DEBUG] Fichiers créés: mail.txt et mail.ok")

            print("🔍 [DEBUG] Vérification des emails terminée")

        except Exception as e:
            print(f"Erreur Graph API lors du traitement du mail : {e}")
            print(f"🔍 [DEBUG] Erreur détaillée: {type(e).__name__}: {str(e)}")


    else:
        print("type de co non géré : attendu IMAP4_SSL, MICROSOFT_EXCHANGE_OWA ou MICROSOFT_EXCHANGE_OAUTH2")
        return


def lire_message(chemin_fichier):
    donnees = {}
    cle_courante = None
    texte_multi_ligne = []

    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            if ligne.startswith('#$'):
                if cle_courante == 'txt' and texte_multi_ligne:
                    donnees['txt'] = '\n'.join(texte_multi_ligne).strip()
                    texte_multi_ligne = []

                cle_val = ligne[2:].split(':', 1)
                cle_courante = cle_val[0].strip()

                if cle_courante == 'txt':
                    texte_multi_ligne.append(cle_val[1].strip())
                else:
                    donnees[cle_courante] = cle_val[1].strip()
            else:
                if cle_courante == 'txt':
                    texte_multi_ligne.append(ligne.rstrip())

    # En fin de fichier, enregistrer le texte si encore en cours
    if cle_courante == 'txt' and texte_multi_ligne:
        donnees['txt'] = '\n'.join(texte_multi_ligne).strip()

    return donnees




def send_mail(expediteur, offusc_conf_agent, destinataire, sujet, contenu_html, piece_jointe_paths=None, serveur="smtp.gmail.com", port=587):
    msg = EmailMessage()
    msg['From'] = expediteur
    msg['To'] = destinataire
    msg['Subject'] = sujet

    # ✅ Définir le contenu HTML comme contenu alternatif
    msg.set_content("Votre client mail ne supporte pas le HTML.")  # fallback texte brut
    msg.add_alternative(contenu_html, subtype='html')

    # ✅ Ajout d'une ou plusieurs pièces jointes si fournie
    if piece_jointe_paths:
        piece_paths = [f for f in os.listdir(piece_jointe_paths) if os.path.isfile(os.path.join(piece_jointe_paths, f))]
        for piece_path in piece_paths:
            try:
                with open(piece_jointe_paths + "/" + piece_path, 'rb') as f:
                    data = f.read()
                    nom_fichier = os.path.basename(piece_jointe_paths + "/" +piece_path)
                    type_mime, _ = mimetypes.guess_type(nom_fichier)
                    maintype, subtype = type_mime.split('/') if type_mime else ('application', 'octet-stream')
                    msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=nom_fichier)
            except Exception as e:
                print(f"Erreur lors de l'ajout de la pièce jointe '{piece_path}': {e}")
    try:
        _, _, mot_de_passe, _, _ = keys_manager.lire_config_imap4_ssl(offusc_conf_agent)
        with smtplib.SMTP(serveur, port) as smtp:
            smtp.starttls()
            smtp.login(expediteur, mot_de_passe)
            smtp.send_message(msg)
        return 0
    except Exception as e:
        print("❌ Une erreur s'est produite :", e)


def check_send_new_emails(offusc_conf_agent,type_co):
    if type_co=="IMAP4_SSL":
        agent, domain, _, _,alias  = keys_manager.lire_config_imap4_ssl(offusc_conf_agent)
        mail = agent+domain
        if alias != "":
            agent = alias
        chemin_dossier_in, chemin_dossier_out = mail_in_folder(agent, "out")
        if os.path.exists(chemin_dossier_out) and os.path.isdir(chemin_dossier_out):
            contenus = os.listdir(chemin_dossier_out)
            if contenus:
                for contenu in contenus:
                    if os.path.exists(chemin_dossier_out + "/" + contenu + "/mail.ok"):
                        chemin = chemin_dossier_out + "/" + contenu + "/mail.txt"
                        infos = lire_message(chemin)
                        # Affichage des informations extraites
                        cles_requises = ["eme", "des", "cop", "pri", "tit", "txt"]
                        if all(cle in infos for cle in cles_requises):
                            send_mail(
                                mail,
                                offusc_conf_agent,
                                infos["eme"],
                                infos["tit"],
                                infos["txt"],
                                piece_jointe_paths= chemin_dossier_out + "/" + contenu + "/pj" #à rajouter quand PJ ok chemin_dossier_out + "/" + contenu + "/pj"
                            )
                            MetManagement.reset_folder(chemin_dossier_in + contenu , recreate=False)
                            MetManagement.reset_folder(chemin_dossier_out + contenu, recreate=False)
                        else:
                            print("il manque des clefs dans le contenu du mail")
            else:
                print("Le dossier est vide.")
        else:
            print("Le dossier n'existe pas ou le chemin n'est pas un dossier.")
    elif type_co=="MICROSOFT_EXCHANGE_OWA":
        try:
            mail, alias, server, username, password, interval_second = keys_manager.lire_config_owa(
                offusc_conf_agent)
            credentials = Credentials(username=username, password=password)
            config = Configuration(server=server,
                                   credentials=credentials)
            account = Account(primary_smtp_address=alias, credentials=credentials, config=config, autodiscover=False,
                              access_type=DELEGATE)
            chemin_dossier_in, chemin_dossier_out = mail_in_folder(alias, "out")
            if os.path.exists(chemin_dossier_out) and os.path.isdir(chemin_dossier_out):
                contenus = os.listdir(chemin_dossier_out)
                if contenus:
                    for contenu in contenus:
                        if os.path.exists(chemin_dossier_out + "/" + contenu + "/mail.ok"):
                            chemin = chemin_dossier_out + "/" + contenu + "/mail.txt"
                            infos = lire_message(chemin)
                            # Affichage des informations extraites
                            cles_requises = ["eme", "des", "cop", "pri", "tit", "txt"]
                            if all(cle in infos for cle in cles_requises):

                                m = Message(
                                    account=account,
                                    folder=account.sent,
                                    subject=infos["tit"],
                                    body=HTMLBody(infos["txt"]),
                                    to_recipients=[Mailbox(email_address=infos["eme"])],
                                    sender=Mailbox(email_address=alias),
                                )
                                m.send_and_save()
                                time.sleep(1)
                                MetManagement.reset_folder(chemin_dossier_in + contenu , recreate=False)
                                MetManagement.reset_folder(chemin_dossier_out + contenu, recreate=False)
                            else:
                                print("il manque des clefs dans le contenu du mail")
                else:
                    print("Le dossier est vide.")




        except Exception as e:
            print(f"Erreur lors du traitement du mail : {e}")
    elif type_co == "MICROSOFT_EXCHANGE_OAUTH2":
        try:
            client_id, client_secret, tenant_id, user_email = keys_manager.lire_config_oauth2(
                offusc_conf_agent)
            # Déduire l'alias pour le nom du dossier
            agent = user_email
            alias = user_email  # tu peux adapter si tu veux un alias distinct plus tard

            chemin_dossier_in, chemin_dossier_out = mail_in_folder(agent, "out")

            authority = f"https://login.microsoftonline.com/{tenant_id}"

            # === Authentification avec MSAL ===
            app = ConfidentialClientApplication(
                client_id=client_id,
                client_credential=client_secret,
                authority=authority
            )
            print("app", app)
            token_result = app.acquire_token_for_client(scopes=["https://outlook.office365.com/.default"])

            if "access_token" not in token_result:
                raise Exception("Impossible d'obtenir un token : ", token_result.get("error_description"))

            token_for_exchangelib = OAuth2Token({
                'access_token': token_result['access_token'],
                'expires_in': token_result.get('expires_in', 3600),
                'token_type': token_result.get('token_type', 'Bearer'),
                'scope': 'https://outlook.office365.com/.default'
            })

            credentials = OAuth2Credentials(
                client_id=client_id,
                client_secret=client_secret,
                tenant_id=tenant_id,
                identity=Identity(primary_smtp_address=user_email),
                access_token=token_for_exchangelib
            )
            config = Configuration(
                credentials=credentials,
                auth_type='OAuth 2.0',
                service_endpoint='https://outlook.office365.com/EWS/Exchange.asmx'
            )

            account = Account(
                primary_smtp_address=user_email,
                config=config,
                autodiscover=False,
                access_type=DELEGATE
            )

            if os.path.exists(chemin_dossier_out) and os.path.isdir(chemin_dossier_out):
                contenus = os.listdir(chemin_dossier_out)
                if contenus:
                    for contenu in contenus:
                        if os.path.exists(chemin_dossier_out + "/" + contenu + "/mail.ok"):
                            chemin = os.path.join(chemin_dossier_out, contenu, "mail.txt")
                            infos = lire_message(chemin)
                            cles_requises = ["eme", "des", "cop", "pri", "tit", "txt"]
                            if all(cle in infos for cle in cles_requises):
                                m = Message(
                                    account=account,
                                    folder=account.sent,
                                    subject=infos["tit"],
                                    body=HTMLBody(infos["txt"]),
                                    to_recipients=[Mailbox(email_address=infos["eme"])],
                                    sender=Mailbox(email_address=alias),
                                )
                                m.send_and_save()
                                time.sleep(1)
                                MetManagement.reset_folder(os.path.join(chemin_dossier_in, contenu), recreate=False)
                                MetManagement.reset_folder(os.path.join(chemin_dossier_out, contenu), recreate=False)
                            else:
                                print("\n\n Il manque des clefs dans le contenu du mail")
                        else:
                            print("\n\n KO § os.path.exists(os.path.join(chemin_dossier_out, contenu)", os.path.exists(os.path.join(chemin_dossier_out, contenu, "mail.ok")))
                else:
                    print("Le dossier est vide.")
            else:
                print("Le dossier n'existe pas ou le chemin n'est pas un dossier.")
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi avec OAuth2 : {e}")
    elif type_co == "MICROSOFT_EXCHANGE_OAUTH2_MICROSOFT_GRAPH":
        try:
            print("📤 [DEBUG] Début de la vérification des emails à envoyer avec Microsoft Graph OAuth2")
            client_id, client_secret, tenant_id, user_email = keys_manager.lire_config_oauth2(
                offusc_conf_agent)
            print(f"📤 [DEBUG] Configuration lue - User: {user_email}, Tenant: {tenant_id}")

            # Déduire l'alias pour le nom du dossier
            agent = user_email
            alias = user_email  # tu peux adapter si tu veux un alias distinct plus tard

            chemin_dossier_in, chemin_dossier_out = mail_in_folder(agent, "out")
            print(f"📤 [DEBUG] Dossiers - In: {chemin_dossier_in}, Out: {chemin_dossier_out}")

            authority = f"https://login.microsoftonline.com/{tenant_id}"

            # === Authentification avec MSAL ===
            app = ConfidentialClientApplication(
                client_id=client_id,
                client_credential=client_secret,
                authority=authority
            )
            print("📤 [DEBUG] Application MSAL créée")

            token_result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

            if "access_token" not in token_result:
                raise Exception("Impossible d'obtenir un token : ", token_result.get("error_description"))

            print("📤 [DEBUG] Token d'accès obtenu avec succès (Client Credentials)")
            access_token = token_result['access_token']
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }

            if os.path.exists(chemin_dossier_out) and os.path.isdir(chemin_dossier_out):
                print("📤 [DEBUG] Dossier de sortie trouvé, lecture du contenu")
                contenus = os.listdir(chemin_dossier_out)
                print(f"📤 [DEBUG] Contenu du dossier: {contenus}")
                if contenus:
                    for contenu in contenus:
                        mail_ok_path = os.path.join(chemin_dossier_out, contenu, "mail.ok")
                        print(f"📤 [DEBUG] Vérification du fichier mail.ok: {mail_ok_path}")
                        if os.path.exists(mail_ok_path):
                            chemin = os.path.join(chemin_dossier_out, contenu, "mail.txt")
                            print(f"📤 [DEBUG] Lecture du message depuis: {chemin}")
                            infos = lire_message(chemin)
                            print(f"📤 [DEBUG] Informations du message lues: {list(infos.keys())}")

                            cles_requises = ["eme", "des", "cop", "pri", "tit", "txt"]
                            if all(cle in infos for cle in cles_requises):
                                print("📤 [DEBUG] Toutes les clés requises sont présentes")
                                print(f"📤 [DEBUG] Envoi vers: {infos['eme']}")
                                print(f"📤 [DEBUG] Sujet: {infos['tit']}")
                                print(f"📤 [DEBUG] Contenu (longueur): {len(infos['txt'])}")

                                # Construire le message pour Microsoft Graph
                                message_data = {
                                    "message": {
                                        "subject": infos["tit"],
                                        "body": {
                                            "contentType": "HTML",
                                            "content": infos["txt"]
                                        },
                                        "toRecipients": [
                                            {
                                                "emailAddress": {
                                                    "address": infos["eme"]
                                                }
                                            }
                                        ]
                                    },
                                    "saveToSentItems": True
                                }

                                # Envoyer l'email via Microsoft Graph
                                send_url = f"https://graph.microsoft.com/v1.0/users/{user_email}/sendMail"
                                print(f"📤 [DEBUG] Envoi via Graph API: {send_url}")
                                try:
                                    response = requests.post(send_url, headers=headers, json=message_data)
                                    response.raise_for_status()
                                    print("📤 [DEBUG] Email envoyé avec succès")
                                except requests.exceptions.HTTPError as e:
                                    if response.status_code == 403:
                                        print("📤 [DEBUG] Erreur 403 - Permissions insuffisantes pour l'envoi")
                                        print("📤 [DEBUG] ==============================================")
                                        print("📤 [DEBUG] ACTION REQUISE - Contactez votre IT Admin:")
                                        print("📤 [DEBUG] ==============================================")
                                        print("📤 [DEBUG] Permission manquante: Mail.Send (Application)")
                                        print("📤 [DEBUG] App: IA-ODATAMINING")
                                        print("📤 [DEBUG] ID: 30ae55f5-f41e-4d44-afcc-082e4b803ba1")
                                        print("📤 [DEBUG] Tenant: 9988c2b8-3feb-4426-aeb7-b8d695bcd025")
                                        print("📤 [DEBUG] ")
                                        print("📤 [DEBUG] INFORMATIONS POUR VOTRE IT ADMIN:")
                                        print("📤 [DEBUG] 1. Azure Portal → Azure AD → App registrations")
                                        print("📤 [DEBUG] 2. Trouver l'app: IA-ODATAMINING")
                                        print("📤 [DEBUG] 3. API permissions → Add permission → Microsoft Graph")
                                        print("📤 [DEBUG] 4. Application permissions → Mail.Send")
                                        print("📤 [DEBUG] 5. Grant admin consent")
                                        print("📤 [DEBUG] ==============================================")
                                        raise Exception(
                                            "❌ Permission Mail.Send manquante. Contactez votre IT Admin pour ajouter cette permission à l'application IA-ODATAMINING.")
                                    else:
                                        raise e

                                time.sleep(1)
                                print("📤 [DEBUG] Nettoyage des dossiers")
                                MetManagement.reset_folder(os.path.join(chemin_dossier_in, contenu), recreate=False)
                                MetManagement.reset_folder(os.path.join(chemin_dossier_out, contenu), recreate=False)
                                print("📤 [DEBUG] Dossiers nettoyés")
                            else:
                                print("\n\n Il manque des clefs dans le contenu du mail")
                                print(
                                    f"📤 [DEBUG] Clés manquantes: {[cle for cle in cles_requises if cle not in infos]}")
                        else:
                            print(
                                f"\n\n KO § os.path.exists(os.path.join(chemin_dossier_out, contenu): {os.path.exists(os.path.join(chemin_dossier_out, contenu, 'mail.ok'))}")
                else:
                    print("Le dossier est vide.")
            else:
                print("Le dossier n'existe pas ou le chemin n'est pas un dossier.")
                print(f"📤 [DEBUG] Chemin vérifié: {chemin_dossier_out}")
                print(
                    f"📤 [DEBUG] Existe: {os.path.exists(chemin_dossier_out)}, Est dossier: {os.path.isdir(chemin_dossier_out) if os.path.exists(chemin_dossier_out) else 'N/A'}")

            print("📤 [DEBUG] Vérification des emails à envoyer terminée")

        except Exception as e:
            print(f"❌ Erreur lors de l'envoi avec Graph API : {e}")
            print(f"📤 [DEBUG] Erreur détaillée: {type(e).__name__}: {str(e)}")
    else:
        print("type de co non valide")

def list_conf_files(type_co):
    conf_files = []
    if type_co is None or type_co == "":
        return conf_files
    dossier = MetManagement.get_secret_content_dir()
    dossier = dossier + type_co
    files = os.listdir(dossier)
    for file in files:
        if file.lower().endswith(".json") or file.lower().endswith(".sec") :
            conf_files.append(file)
    return conf_files



if __name__ == "__main__":
    type_co="IMAP4_SSL"
    list_agent_email = []
    offusc_conf_agents = list_conf_files(type_co)
    while True:
        for offusc_conf_agent in offusc_conf_agents:
            print("offusc conf agent : ", offusc_conf_agent)
            check_new_emails(offusc_conf_agent,type_co, list_agent_email)
            time.sleep(1)
            check_send_new_emails(offusc_conf_agent,type_co)
            time.sleep(1)
