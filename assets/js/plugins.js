// place any jQuery/helper plugins in here, instead of separate, slower script files.

// Requests:
/*
fetch documentation - https://fetch.spec.whatwg.org/#fetch-api
*/
// Fetch because it has promises and is easier to setup.

function processJSON(json){
  // TODO: handle errors here.
  // TODO: all logic for processing response
   console.log(json)
  // console.log(json.args)
//  console.log(json.args.param1)
  // console.log(json.headers)
  return json
}

function fetchGet(apiUrl, params) {
  console.log('Getting from', apiUrl)
  var url = new URL(apiUrl)

  // set parameters to URL request
  Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))

  processedResponse = fetch(url, {
    method: 'GET'
  })
//  .then(response => response.json())
  .then(processJSON);

  return processedResponse
}

function fetchPost(apiUrl, params, data) {
  console.log('Posting to', apiUrl)
  var url = new URL(apiUrl)

  // set parameters to URL request
  Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))

  processedResponse = fetch(url, {
    method: 'POST',
    // TODO: all metadata goes in headers
//    headers : {
//        'Content-Type': 'application/json',
//        'Accept': 'application/json'
//       },
    body: JSON.stringify(data),
  })
  .then(response => response.json())
  .then(processJSON);
    console.log(processedResponse)

  // TODO: add status check (200)

  return processedResponse
}


function fetchPost1(apiUrl, params, data) {
  console.log('Inside fetchPost1 for', apiUrl)
  var url = new URL(apiUrl)

  // set parameters to URL request
  Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))

  processedResponse = fetch(url, {
    method: 'POST',
    body: JSON.stringify(data),
  })
  .then(response => response.text())

  console.log(processedResponse)

  return processedResponse
}


// fetch('https://jsonplaceholder.typicode.com/todos/1')
//   .then(response => response.json())
//   .then(json => console.log(json))





//Cookie logic
function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    console.log('cookie set', name)
}
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        // console.log(c);
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
function eraseCookie(name) {
    document.cookie = name+'=; Max-Age=-99999999;';
}

setCookie('ppkcookie','testcookie',7);
document.cookie = 'tset'
cook = document.cookie;
console.log("cookie:", cook)
var x = getCookie('ppkcookie');
if (x) {
  console.log(x)
}
console.log(x)



// Like button
$(".like-button").on("click", function(e){
    var $counter = $(this).find(".count"); // finds count var in this HTML element
    var count = $counter.text() | 0; //corose current count to an int
    $counter.text(count + 1);//set new count

//    apiUrl = 'https://httpbin.org/get'; // TODO: change from global variable later
//    fetchGet(apiUrl, {param1:count, param2:2})
//    fetchPost(apiUrl, {param1:count, param2:2}, {body_data: count})


    // Send a POST request
    apiUrl = 'http://0.0.0.0:5000/users/tip'
    // TODO: add cookie here too
    fetchPost1(apiUrl, {}, {'amount': 1, 'merchant_id': 1})
    console.log('Reached button')
});


$(".cookie-button").on("click", function(e){
    var $cookie = $(this).find(".cookie"); // finds count var in this HTML element
    apiUrl = 'https://httpbin.org/users/cookie'; // TODO: change from global variable later
    var response = fetchGet(apiUrl, {})
    console.log(response.cookie)
});
