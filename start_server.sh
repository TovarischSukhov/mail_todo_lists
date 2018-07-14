docker stop mail_index && docker rm mail_index
docker run --name mail_index -d -v ${PWD}/nginx:/etc/nginx/conf.d -v ${PWD}/static:/usr/share/nginx/html:ro -p 1249:1249 nginx