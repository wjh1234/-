#!/usr/bin/env bash
# Script Name:  run-app.sh
# Function:     JBOSS   服务应用的统一启动脚本

# 用户自定义选项
FRAMEWORK_DIR="/opt/jboss-eap"      # srm 根目录
BASE_DIR="/opt/apps"            	# war 包根目录
DPAP_DIR="/opt/oms-common"

# 保持系统环境变量编码
export LC_ALL=en_US.UTF-8

# -o或--options选项后面接可接受的短选项，如ab:c::，表示可接受的短选项为-a -b -c，其中-a选项不接参数，-b选项后必须接参数，-c选项的参数为可选的
# -l或--long选项后面接可接受的长选项，用逗号分开，冒号的意义同短选项。
# -n选项后接选项解析错误时提示的脚本名字
ARGS=`getopt -o en:o:u:s:: --long enable_http,name:,offset:,uri:,steps:: -n 'run-app.sh' -- "$@"`
if [ $? != 0 ]; then
    echo "Terminating..."
    exit 1
fi

# 将规范化后的命令行参数分配至位置参数（$1,$2,...)
eval set -- "${ARGS}"

while true
do
    case "$1" in
        -n|--name)
            APP_NAME=$2
            echo "config: application_name => ${APP_NAME}"
            shift 2
            ;;
        -o|--offset)
            OFFSET=$2
            echo "config: port_offset => ${OFFSET}"
            shift 2
            ;;
        -u|--uri)
            URI=$2
            echo "config: http_uri => ${URI}"
            shift 2
            ;;
        -s|--steps)
            case "$2" in
                "")
                    STEPS=12
                    echo "config: max_check_steps => ${STEPS}"
                    shift 2
                    ;;
                *)
                    STEPS=$2
                    echo "config: max_check_steps => ${STEPS}"
                    shift 2;
                    ;;
            esac
            ;;
        -e|--enable_http)
            HTTP_FLAG=true
            echo "config: enable_http => true"
            shift
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Internal error!"
            exit 1
            ;;
    esac
done

if [[ ! ${APP_NAME} || ! ${OFFSET} ]]; then
    usage="Usage: \n
    -n | --name, 指定应用的名称 \n
    -o | --offset, 指定应用端口的偏移量 \n
    -s | --steps, 指定应用启动后的检测间隔, 每一个间隔 sleep 5秒, 默认为 12, 即 1 分钟 \n
    -e | --enable_http, 启用 HTTP 检测 \n
    -u | --uri, 当启用 HTTP 检测时, 需要自定访问的 uri"
    echo -e ${usage}
    exit 1
fi

if [[ "${HTTP_FLAG}" = true ]]; then
    if [[ -z ${URI} ]]; then
      echo "当启用 HTTP 检测时, 需要使用 -u | --uri 指定访问的 uri"
      exit 1
    fi
fi

APP_DIR="${BASE_DIR}/${APP_NAME}"

# 项目环境变量 
env_config="${APP_DIR}/deployments/env_config"
if [[ -f $env_config ]]; then
  source $env_config 
else
  echo "没有检测到环境变量配置文件: $env_config, 启动失败"
  exit 1
fi

# stop application(s) before restart it 
running_pid=`ps aux | grep ${APP_NAME}/configuration | grep -v grep | awk '{print $2}'`
for pid in ${running_pid}; do
    kill -9 ${pid}
done

cat /dev/null > ${APP_DIR}/log/nohup.out

rm -rf ${APP_DIR}/tmp/*
rm -rf ${APP_DIR}/data/*

nohup ${FRAMEWORK_DIR}/bin/standalone.sh \
-Dglobal.config.path=${DPAP_DIR}/dpap-config/ \
-Djboss.server.base.dir=${APP_DIR} \
-c=${APP_NAME}.xml -b "0.0.0.0" \
-Djboss.socket.binding.port-offset=${OFFSET} \
-Dorg.jboss.as.logging.per-deployment=false \
-Dfile.encoding=utf-8 > ${APP_DIR}/log/nohup.out 2>&1 &

#sleep 5
#tail /opt/jboss/${APP_NAME}/log/server.log
#tail -f /opt/jboss/${APP_NAME}/log/nohup.out|grep "/started in/Q"

# 进程检查
started=0
for k in $( seq 1 ${STEPS} )
do
    ps aux | grep ${APP_NAME}/configuration | grep -v grep > /dev/null 2>&1
    if [[ $? -eq 0 ]]; then
        echo "start the application successful"
        started=1
    break
    fi

    sleep 5
done

if [[ ${started} -eq 0 ]]; then
    echo "start the application failed"
    exit 1
fi

# HTTP 状态检查
if [[ "${HTTP_FLAG}" = true ]]; then
    port=$[ 8080 + ${OFFSET} ]
    url="http://127.0.0.1:$port/${URI}"
    http_status=`curl --connect-timeout 60 -sL ${url} -w "%{http_code}" -o /dev/null`

    if [[ "${http_status}" = "200" ]]; then
        echo "http request successful"
    else
        echo "http request failed"
        exit 1
    fi
fi
