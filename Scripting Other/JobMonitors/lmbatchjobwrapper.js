if (WScript.Arguments.length < 4) {
    showUsage();
    WScript.Quit(1);
}

//WScript.Echo("Arg1: " + WScript.Arguments(0));
//WScript.Echo("Arg2: " + WScript.Arguments(1));
//WScript.Echo("Arg3: " + WScript.Arguments(2));
//WScript.Echo("Arg4: " + WScript.Arguments(3));

var agentAddr = WScript.Arguments(0);
var hostName = WScript.Arguments(1);
var jobName = WScript.Arguments(2);
var cmdLine = WScript.Arguments(3);

var agentUrl = formUrl(agentAddr);
var executionNo = new Date().getTime();

//WScript.Echo(agentUrl);

sendStart(agentUrl, hostName, jobName, cmdLine, executionNo);

var result = runCmd(cmdLine);

//WScript.Echo("\nExitCode: " + result.exitCode);

//WScript.Echo("\nStdOut:");
//WScript.Echo(result.stdout);

//WScript.Echo("\nStdErr:");
//WScript.Echo(result.stderr);

sendResult(agentUrl, hostName, jobName, executionNo, result);

function showUsage() {
    WScript.Echo("cscript.exe lmbatchjobwrapper.js <agentaddr> <hostname> <jobname> <cmdline>");
    WScript.Echo("Example:");
    WScript.Echo("         cscript.exe lmbatchjobwrapper.js 10.1.1.1:7214 host myJob \"cmd.exe /C dir\"");
}
;

function runCmd(cmdLine) {
    var result = {};
    result.stdout = "";
    result.stderr = "";
    result.exitCode = -1;

    var wshShell = new ActiveXObject("WScript.Shell");
    if (!wshShell) {
        WScript.Echo("Can not run command");
        result.userdata = "Can not run command";
        return result;
    }

    var oExec;
    try {
        oExec = wshShell.Exec(cmdLine);
    }
    catch (e) {
        WScript.Echo("Unable to run command - " + cmdLine);
        result.userdata = "Unable to run command";
        return result;
    }

    var line;
    while (oExec.Status != 1) {
        while (!oExec.StdOut.AtEndOfStream) {
            line = oExec.StdOut.ReadLine();
            result.stdout += line + "\n";
        }
        while (!oExec.StdErr.AtEndOfStream) {
            line = oExec.StdErr.ReadLine();
            result.stderr += line + "\n";
        }
        WScript.Sleep(100);
    }

    result.exitCode = oExec.ExitCode;

    return result;
}
;

function formUrl(agentAddr) {
    var url = "http://" + agentAddr + "/batchjobhandler/reportEvent";
    return url;
}
;

function sendStart(agentUrl, hostName, jobName, cmdLine, executionNo) {
    // type=start|finish&executionNo=xxx&hostName=xxx&batchjobName=xxx&epoch=(time in
    // seconds since 1970.1.1)&exitCode=xxx&cmdLine=xxx&stdout=xxxx&stderr=xxx&userData=xxx&alertLevel=xxxx

    var payload = "type=start";
    payload += "&executionNo=" + executionNo;
    payload += "&hostName=" + encodeURIComponent(hostName);
    payload += "&batchjobName=" + encodeURIComponent(jobName);
    payload += "&epoch=" + parseInt(new Date().getTime() / 1000);
    payload += "&cmdLine=" + encodeURIComponent(cmdLine);

    // Create XMLHTTP instance
    var oHttp = new ActiveXObject("MSXML2.XMLHTTP");
    if (!oHttp) {
        WScript.Echo("Unable to send HTTP request.");
        WScript.Quit(4);
    }

    try {
        // Open a POST connection to the agentHttpService
        oHttp.open("post", agentUrl, false);

        // Set HTTP headers
        oHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        //WScript.Echo("Sending: " + payload);

        // Send the result
        oHttp.send(payload);
    }
    catch (e) {
        WScript.Echo("Unable to connect to the server.");
        WScript.Quit(5);
    }

    //WScript.Echo(oHttp.status);
    //WScript.Echo(oHttp.responseText);

    if (oHttp.status != 200) {
        WScript.Echo("Not a valid server.");
        WScript.Quit(6);
    }
}
;

function sendResult(agentUrl, hostName, jobName, executionNo, result) {
    // type=start|finish&executionNo=xxx&hostName=xxx&batchjobName=xxx&epoch=(time in
    // seconds since 1970.1.1)&exitCode=xxx&cmdLine=xxx&stdout=xxxx&stderr=xxx&userData=xxx&alertLevel=xxxx

    var payload = "type=finish";
    payload += "&executionNo=" + executionNo;
    payload += "&hostName=" + encodeURIComponent(hostName);
    payload += "&batchjobName=" + encodeURIComponent(jobName);
    payload += "&epoch=" + parseInt(new Date().getTime() / 1000);
    payload += "&exitCode=" + result.exitCode;
    payload += "&stdout=" + encodeURIComponent(result.stdout);
    payload += "&stderr=" + encodeURIComponent(result.stderr);
    if (result.userdata) {
        payload += "&userData=" + encodeURIComponent(result.userdata);
    }
    payload += "&alertLevel=" + ((0 == result.exitCode) ? "ok" : "error");

    // Create XMLHTTP instance
    var oHttp = new ActiveXObject("MSXML2.XMLHTTP");
    if (!oHttp) {
        WScript.Echo("Unable to send HTTP request.");
        WScript.Quit(4);
    }

    try {
        // Open a POST connection to the agentHttpService
        oHttp.open("post", agentUrl, false);

        // Set HTTP headers
        oHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        //WScript.Echo("Sending: " + payload);

        // Send the result
        oHttp.send(payload);
    }
    catch (e) {
        WScript.Echo("Unable to connect to the server.");
        WScript.Quit(5);
    }

    //WScript.Echo(oHttp.status);
    //WScript.Echo(oHttp.responseText);

    if (oHttp.status != 200) {
        WScript.Echo("Not a valid server.");
        WScript.Quit(6);
    }
}
;