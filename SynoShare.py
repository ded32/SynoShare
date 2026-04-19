#=========================================================================
# SynoShare.py (c) Ded, 2020
#=========================================================================

from __future__ import print_function;
import requests;
import urllib3;
import json;
import traceback;
import sys;
import os;

#=========================================================================

NAS     = str (os.getenv (".SynoShareNAS"));
Account = str (os.getenv (".SynoShareAccount"));
Passwd  = str (os.getenv (".SynoSharePasswd"));

LinkCreated    = 0;
LinkExists     = 1;
LinkNotCreated = 2;
FatalError     = 3;
SyntaxError    = 255;

#-------------------------------------------------------------------------

Sid = "";

Debug = False;
if (len (sys.argv) >= 3): Debug = (sys.argv[2] == "--debug");

urllib3.disable_warnings();

#=========================================================================

def main():
    #
    _("", "main()");

    file = "";
    if (len (sys.argv) >= 2): file = sys.argv[1];

    if (file == ""):
        #
        eprint ("ERROR: Usage: " + sys.argv[0] + " <path/filename to share> [--debug]");
        return SyntaxError;
        #

    if (NAS == "None" or Account == "None" or Passwd == "None"):
        #
        eprint ("ERROR: .SynoShareNAS, .SynoShareAccount or .SynoSharePasswd environment variable(s) NOT found");
        return SyntaxError;
        #

    DoAuth (Account, Passwd);

    list = SharingList();

    links = list["data"]["links"];
    total = list["data"]["total"];

    for (link) in (links):
        #
        if (link["path"] == file):
            #
            url = _(link["url"], "url");

            eprint ("EXISTS:", url);
            print (url);
            return LinkExists;
            #
        #

    url  = "";
    link = _(SharingCreate (file), "link");

    if (link["success"] == True):
        #
        url = _(link["data"]["links"][0]["url"], "url");
        eprint ("CREATED:", url);
        print (url);
        return LinkCreated;
        #
    else:
        #
        eprint ("NOT created:", '"' + file + '"');
        return LinkNotCreated;
        #
    #

#=========================================================================

def GetApiInfo():
    #
    _("\n", "GetApiInfo()");

    return _(Get ("query.cgi?api=SYNO.API.Info&version=1&method=query&query=SYNO.API.Auth,SYNO.FileStation"), "GetApiInfo");
    #

#-------------------------------------------------------------------------

def DoAuth (account, passwd):
    #
    _("\n" + "account = " + account + ", passwd = " + passwd, "DoAuth()");

    try:
        #
        account = Decode (account);
        passwd  = Decode (passwd);

        res = _(Get ("auth.cgi?api=SYNO.API.Auth&version=3&method=login&account=" + account + "&passwd=" + passwd + "&session=FileStation&format=sid"), "DoAuth()");

        global Sid;
        Sid = res["data"]["sid"];

        return _(Sid, "DoAuth(): Sid");
        #

    except Exception as e:
        raise Exception ('DoAuth(): Cannot auth in "' + NAS + '":\n  ' + str (e));
    #

#-------------------------------------------------------------------------

def SharingList():
    #
    _("\n", "SharingList()");

    return _(Get ("entry.cgi?api=SYNO.FileStation.Sharing&version=3&method=list"), "DoSharing");
    #

#-------------------------------------------------------------------------

def SharingCreate (path):
    #
    _("\n" + "path = " + path, "SharingCreate()");

    return _(Get ('entry.cgi?api=SYNO.FileStation.Sharing&version=3&method=create&path="' + path + '"'), "DoSharing");
    #

#=========================================================================

def Get (request):
    #
    _("\n" + "request = " + request, "Get()");

    if (Sid != ""): request += "&_sid=" + Sid;

    res = _(requests.get (verify = False, url = _("http://" + NAS + "/webapi/" + request, "GET")), "GET");
    if (res.status_code != 200):  raise Exception ("Get (" + request + "): Bad status " + str (res.status_code) + ":\n  " + res.text);

    res = json.loads (res.text);
    if (not res["success"]): raise Exception ("Get (" + request + "):\n" + "  Error: " + StrError (res["error"]["code"]));

    return _(res, "GOT");
    #

#-------------------------------------------------------------------------

def StrError (code):
    #
    errlist = { 400: "No such account or incorrect password",
                401: "Account disabled",
                402: "Permission denied",
                403: "2-step verification code required",
                404: "Failed to authenticate 2-step verification code",
               2000: "Sharing link does not exist",
               2001: "Cannot generate sharing link because too many sharing links exist",
               2002: "Failed to access sharing links" };

    return str (code) + ": " + errlist.get (code, "Unknown error");
    #

#-------------------------------------------------------------------------

def Decode (str):
    #
    _("str = " + str, "Decode()");

    decoded = "";

    i = 0;
    for (c) in (str):
        #
        decoded += chr ((~(ord (c) - 32) ^ i) % (128-32) + 32);
        i += 1;
        #

    return decoded;
    #

#=========================================================================

def _ (data = "", name = ""):
    #
    if (not Debug): return data;

    if (str (data) [0:1] == "\n"): data = data[1:]; eprint();

    if (name != ""): eprint (name, ": ", sep = "", end = "");

    if (data != ""): eprint ('"', data, '"', sep = "");
    else: eprint();

    return data;
    #

#-------------------------------------------------------------------------

def eprint (*args, **kwargs):
    #
    print (*args, file=sys.stderr, **kwargs)
    #

#=========================================================================

try:
    sys.exit (main());

except Exception as e:
    #
    eprint ("ERROR: " + str (e));
    if (Debug): eprint ("\n" + traceback.format_exc());
    sys.exit (FatalError);
    #
