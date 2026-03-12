import os
from dotenv import load_dotenv
from github import Github, Auth, GithubException
from github_error_codes import GithubInviteCode

def inviter_utilisateur(username):
    load_dotenv()

    TOKEN = os.getenv("GITHUB_TOKEN")
    ORG_NAME = os.getenv("ORG_NAME")

    if not TOKEN:
        print("Erreur: GITHUB_TOKEN manquant dans le .env")
        return GithubInviteCode.CONFIG_MISSING_TOKEN

    auth = Auth.Token(TOKEN)
    g = Github(auth=auth)
    org = g.get_organization(ORG_NAME)

    # On vérifie si l'utilisateur existe
    try:
        user = g.get_user(username)
    except GithubException:
        print(f"L'utilisateur {username} n'existe pas sur GitHub.")
        return GithubInviteCode.USER_NOT_FOUND
    
    # On vérifie si l'utilisateur est déjà membre de l'organisation
    if org.has_in_members(user):
        print(f"{username} est déjà membre de l'organisation.")
        return GithubInviteCode.USER_ALREADY_MEMBER
    
    invitations = org.invitations()

    # On vérifie s'il y a déjà une invitation en attente pour cet utilisateur
    for invitation in invitations:
        if invitation.login == username:
            print(f"{username} a déjà une invitation en attente.")
            return GithubInviteCode.USER_ALREADY_INVITED

    # Si toutes les vérifications sont passées sans problème, on envoie l'invitation à l'utilisateur
    try:
        org.invite_user(user=user)
        print(f"Invitation envoyée à {username}")
        return GithubInviteCode.OK
    except GithubException as e:
        print(f"Erreur GitHub: {e}")
        return GithubInviteCode.GITHUB_API_ERROR
    except Exception as e:
        print(f"Erreur : {e}")
        return GithubInviteCode.UNKNOWN_ERROR

if __name__ == "__main__":
    inviter_utilisateur("username")