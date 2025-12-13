const { contextBridge } = require("electron");

function printOutFile(file, printerSpec) {

}

contextBridge.exposeInMainWorld("printer", {putOut: printOutFile});
