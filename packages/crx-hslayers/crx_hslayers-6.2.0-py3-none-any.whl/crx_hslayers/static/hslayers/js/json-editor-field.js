"use strict";

var editorObserver = new MutationObserver(function (mutationRecords) {
    let editorId = undefined;
    for (let i = 0; mutationRecords.length !== i; i++) {
        editorId = getEditorId(mutationRecords[i]);
        if (editorId) {
            initEditor(editorId);
            return;
        }
    }
});

function getEditorId(mutationRecord) {
    let addedNode = {};
    if (mutationRecord.addedNodes.length > 0) {
        for (let i = 0; mutationRecord.addedNodes.length !== i; i++) {
            addedNode = mutationRecord.addedNodes[i]

            if (addedNode.classList && addedNode.classList.contains("json-editor-id")) {
                return addedNode.value;
            }
        }
    }
    return undefined;
}



function initEditor(editorId) {
    
    let editorElement = document.getElementById(editorId + "-editor");
    let input = document.getElementById(editorId);
    let jsonParsed = JSON.parse(input.value);

    const editor = new JSONEditor(editorElement, {        
        disable_collapse: true,
        disable_edit_json: true,
        disable_properties: true,           
        schema: {
            type: "object",
            title: "settings",
            properties: prepareSchema(jsonParsed),                     
        }
    })

    editor.on('change', () => {
        input.value = JSON.stringify(editor.getValue());
    });

}

function prepareSchema(jsonObject) {
    var schema = {};

    for (var key in jsonObject) {
        schema[key] = {};
        schema[key].type = typeof (jsonObject[key]);

        if (typeof (jsonObject[key]) === "object") {            
            schema[key].properties = prepareSchema(jsonObject[key]);
        }
        else {

            if (typeof (jsonObject[key]) === "boolean") {
                schema[key].format = "checkbox";
            }

            schema[key].default = jsonObject[key];
        }
    }    
    return schema;
}




document.addEventListener("DOMContentLoaded", function (event) {
    editorObserver.observe(document, { childList: true, subtree: true });

    let editorNodes = document.querySelectorAll(".json-editor-id");
    for(let i = 0; editorNodes.length !== i; i++){
        initEditor(editorNodes[i].value);
    }
});


