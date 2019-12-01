#!/bin/bash
echo

check_dep() {
    if command -v $1 >/dev/null 2>&1 ; then
        echo "$1 found, version:"
        $1 --version
    else
        echo "$1 not found"
        echo "check out $2"
        echo
        exit 1
    fi
    echo
}

check_dep make https://www.gnu.org/software/make/
check_dep python https://www.python.org/
check_dep virtualenv https://virtualenv.pypa.io/en/latest/
check_dep docker https://www.docker.com/
check_dep docker-compose https://docs.docker.com/compose/
check_dep protoc https://developers.google.com/protocol-buffers
check_dep capnp https://capnproto.org/
