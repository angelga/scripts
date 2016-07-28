#
# pip install should only be executed under virtualenv to prevent global installs
#
export PIP_REQUIRE_VIRTUALENV=true
gpip(){
   PIP_REQUIRE_VIRTUALENV="" pip "$@"
}
