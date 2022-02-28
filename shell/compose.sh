# params
# 1: output filename
# 2: env vars to pass to compose
var_list=($2)
# starting part
cat << EOF >> $1
  $APP_NAME:
    build: ./src
    container_name: ${APP_NAME}
    restart: always
    environment:
$(for env_var in "${var_list[@]}" ; do
    if [[ ${env_var} == *"CORS"* ]]; then
      break
    else
      echo "      - ${env_var}";
    fi
  done)
    expose:
      - ${SOCKET_PORT}
$(if [[ -z ${MODEL_TYPE} ]]; then
    echo "    command: uvicorn ${FILE_NAME}:app --host 0.0.0.0 --port ${SOCKET_PORT}"
  elif [[ ${MODEL_TYPE} == "OPENVINO" ]]; then
    echo '    command: bash -c "source /opt/intel/openvino_2021/bin/setupvars.sh && uwsgi uwsgi.ini" '
  fi)
    volumes:
      - ./src:/app



EOF

