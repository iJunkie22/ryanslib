
function coda_find() {
    var q_text = '--' + this.textContent + '-->';
    console.log(CodaTextView.path());
    
    var user_home = CodaTextView.path().split("/", 5).join("/");
    var q_res = CodaPlugInsController.runCommand(user_home + "/Library/Application Support/Coda 2/Plug-ins/SiteHTMLSidebar.codawebscriptsidebar/codagrep.sh", [q_text, CodaTextView.path()]);
    CodaTextView.goToLineAndColumn(q_res, 0);
    CodaTextView.setSelectedRange(CodaTextView.rangeOfCurrentLine());
    //console.log(q_com);
    console.log(q_res);
}

function init_doc() {
    var parser = new DOMParser();
    var d3 = parser.parseFromString(CodaTextView.string(), "text/html");
    return d3;
}

function getComments(doc, elem) {
    var iterator = doc.createNodeIterator(elem, NodeFilter.SHOW_COMMENT);
    var comments = [];
    var curNode;
    while (curNode = iterator.nextNode()) {
        comments.push(curNode.nodeValue);
    }
	
	return comments;
}

function refresh_globals_list() {
    var doc1 = init_doc();
    var coms = getComments(doc1, doc1.documentElement);
    
    var globals_ol = document.getElementById("globals_list");
    var globals_children = globals_ol.childNodes;
    if (globals_children) {
        var ol_len = globals_children.length;
        for (var i = ol_len; i > 0; i--) {
            var x = globals_children[i - 1];
            globals_ol.removeChild(x);
        }
    }
    
    
    for (var i=0; i < coms.length; i++) {
        var x = coms[i];
        var com_str = String(x.trim());
        if ((com_str.indexOf('Begin Global') == 0) || (com_str.indexOf('End Global') == 0)) {
            var new_li = document.createElement('li');
            var new_a = document.createElement('a');
            new_a.href = "#";
            new_a.textContent = x;
            new_a.onclick = coda_find;
            new_li.appendChild(new_a);
            globals_ol.appendChild(new_li);
        }
        
    }
    
}

function textViewWillSave(CodaTV) {
    refresh_globals_list();
}

