import git 
g = git.Git('/home/tom87/cicdrone/')
hexshas = g.log('--pretty=%H','--follow','--',filename).split('\n')
print (hexshas)
