.PHONY: sync
sync:
	rsync -avzh -e "ssh -i ~/.ssh/id_rsa1" --exclude .git --exclude .venv --exclude __pycache__ . root@146.190.32.178:/srv/vpp-sandbox/vmanage-agent
