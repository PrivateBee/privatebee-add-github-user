import os
from dotenv import load_dotenv
from github import Github, Auth, GithubException

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
ORG_NAME = "PrivateBeeTEST"

# TODO: renvoyer des codes d'erreur au bot discord pour qu'il transmette un message à l'utilisateur
def inviter_utilisateur(username):
    auth = Auth.Token(TOKEN)
    g = Github(auth=auth)
    org = g.get_organization(ORG_NAME)

    # On vérifie si l'utilisateur existe
    try:
        user = g.get_user(username)
    except GithubException:
        print(f"L'utilisateur {username} n'existe pas sur GitHub.")
        return
    
    # On vérifie si l'utilisateur est déjà membre de l'organisation
    if org.has_in_members(user):
        print(f"{username} est déjà membre de l'organisation.")
    
    invitations = org.invitations()

    # On vérifie s'il y a déjà une invitation en attente pour cet utilisateur
    for invitation in invitations:
        if invitation.login == username:
            print(f"{username} a déjà une invitation en attente.")
            return

    # Si toutes les vérifications sont passées sans problème, on envoie l'invitation à l'utilisateur
    try:
        org.invite_user(user=user)
        print(f"Invitation envoyée à {username}")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    # TODO: ici mettre à jour pour le bot discord
    inviter_utilisateur("username")