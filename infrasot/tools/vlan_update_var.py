import git
import difflib
import hashlib

def compare_git_file_with_local(repo_path: str, file_path: str, last_state_path:str):
    try:
        g = git.Git(repo_path)
        repo = git.Repo(repo_path)
        commit_count = 0
        
        # Récupérer la liste des commits affectant le fichier
        hexshas = g.log('--pretty=%H', '--follow', '--', file_path).split('\n')
        
        # Ouvrir le fichier d'état actuel
        with open(last_state_path, 'r', encoding='utf-8') as last_state:
            last_state_content = last_state.read()
        hash_last_state = hashlib.md5(last_state_content.encode('utf-8')).hexdigest()
        
        # Comparer avec les versions du fichier dans Git
        for commit_hash in hexshas:
            commit = repo.commit(commit_hash)
            file_content = commit.tree[file_path].data_stream.read().decode('utf-8')
            hash_commit = hashlib.md5(file_content.encode('utf-8')).hexdigest()
            
            if hash_last_state == hash_commit:
                print(f"Le fichier local et la version du commit {commit_hash} sont identiques et vous êtes à"+str(commit_count)+" commit de l etat actuel")
                break
            else:
                commit_count +=1
                print(f"Le fichier local et la version du commit {commit_hash} sont différents.")
    except Exception as e:
        print(f"Erreur : {e}")

# Exemple d'utilisation
repo_path = "/home/tom87/cicdrone/"  # Remplacez par votre dépôt Git
file_path = "infrasot/vlan_list.yml"  # Remplacez par le fichier à comparer
last_state_path = "/home/tom87/cicdrone/infrasot/archive/vlan_list_last_state.yml"

compare_git_file_with_local(repo_path, file_path, last_state_path)
