(function() {
    butt = document.getElementById('diagram-download')
    butt.addEventListener('click', function(e) {
        const out$ = this || window;
        svgEl = document.querySelector(".mermaid svg");
        svgEl.setAttribute("xmlns", "http://www.w3.org/2000/svg");
        const svgData = svgEl.outerHTML.replaceAll("<br>", "<br/>").replaceAll(/<img([^>]*)>/g, (ee,re)=>`<img ${re} />`);
        var preface = '<?xml version="1.0" standalone="no"?>\r\n';
        var svgBlob = new Blob([preface, svgData], {type:"image/svg+xml;charset=utf-8"});
        var svgUrl = URL.createObjectURL(svgBlob);
        var downloadLink = document.createElement("a");
        downloadLink.href = svgUrl;
        downloadLink.download = name;
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
    });
})();
