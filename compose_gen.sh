rm -rf docker-compose.yml

# start
# generate the version and services part
cat << EOF >> docker-compose.yml
version: "3.7"

services:

EOF

# loop api list
for service in $(cat api_list.txt) ; do
  # convert name to directory
  d="${service##*/}/"
  # here first we get the service .env vars
  if [ -f "${d}.env" ]
  then
    # here we also need flask and uwsgi port setting port and app name
    # so lets not change this for now since appending to the list will take debugging
    var_list=$(cat ${d}.env | sed 's/#.*//g' | xargs)
    export $var_list
    echo "[INFO] adding ${d} to docker compose"
    chmod +x shell/compose.sh
    # here we can optionally add which part of the env params we want to be added to the compose file
     ./shell/compose.sh docker-compose.yml "${var_list}"
    # unset to avoid bugs from specific env vars
    for line in $var_list
    do
      # split here to get var names and unset them
      IFS='=' read -a array <<< "${line}"; unset "${array[0]}"
    done
    # unset MODEL_TYPE
  else
    # no .env file then quit
    echo "[ERROR] .env file not found for ${d}! exiting.."
    exit 64
  fi
done

