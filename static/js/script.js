// Function to load imagers Asynchronously
function preloadCallback(src, elementId) {
    var img = document.getElementById(elementId)
    img.src = src
}

function preloadImage(imgSrc, elementId) {
    // console.log("attempting to load " + imgSrc + " on element " + elementId)
    var objImagePreloader = new Image();
    objImagePreloader.src = imgSrc;
    if (objImagePreloader.complete) {
        preloadCallback(objImagePreloader.src, elementId);
        objImagePreloader.onload = function () {
        };
    } else {
        objImagePreloader.onload = function () {
            preloadCallback(objImagePreloader.src, elementId);
            //    clear onLoad, IE behaves erratically with animated gifs otherwise
            objImagePreloader.onload = function () {
            };
        }
    }
}

// function to validate text and render it as markdown
function validateText(str) {
    var md = window.markdownit({
        highlight: function (str, lang) {
            if (lang && hljs.getLanguage(lang)) {
                try {
                    return '<pre class="hljs"><code>' +
                        hljs.highlight(lang, str, true).value +
                        '</code></pre>';
                } catch (__) {
                }
            }
            return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>';
        },
        linkify: true,
    });
    var result = md.render(str);
    return result
}


// ----->  account/account.html
