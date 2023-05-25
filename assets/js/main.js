let SenderUser = document.getElementById("senderuser");
let userchat = document.getElementById("userchat");

if (SenderUser == null)
	SenderUser = document.getElementById("my_username").value
else{
	SenderUser = document.getElementById("senderuser").value
}

if (userchat == null)
	userchat = "Unnknown"
else{
	userchat = document.getElementById("userchat").value
}

var loc = window.location;
var wsStart = 'ws://';
if (loc.protocol == 'https:') {
     wsStart = 'wss://'
}


var endpoint = wsStart + loc.host + '/ws/chat/' + userchat + "/" + SenderUser + "/";

const chatSocket = new ReconnectingWebSocket(endpoint);


function get_message(e) {
  var elem = $(e);
  var start = elem.data("start");
  var end = elem.data("end");
  if (start == 0 && end == 0) {
    start = $(".message-body").length;
    end = start + 5;
    elem.data("start", $(".message-body").length);
    elem.data("end", start + 5);
  }
  chatSocket.send(
    JSON.stringify({
      command: "fetch_message",
      start: start,
      end: end,
    })
  );
  elem.data("start", end);
  elem.data("end", end + 5);
}

chatSocket.onopen = function (e) {
	if (userchat != "Unnknown"){
		chatSocket.send(
			JSON.stringify({
				command: "fetch_message_unread",
			})
		);
	}
};

chatSocket.onclose = function (e) {
  console.error("Chat socket closed unexpectedly");
};

if (document.querySelector("#chat-message-input") != null)
	document.querySelector("#chat-message-input").focus();
// document.querySelector("#chat-message-input").onkeyup = function (e) {
//   if (e.keyCode === 13) {
//     // enter, return
//     document.querySelector("#chat-message-submit").click();
//   }
// };

if (document.querySelector("#chat-message-submit") != null){
	document.querySelector("#chat-message-submit").onclick = function (e) {
		const messageInputDom = document.querySelector("#chat-message-input");
		const message = messageInputDom.value;
		chatSocket.send(
			JSON.stringify({
				"command": "new_message",
				"from_user_username": SenderUser,
				"sender_chat_username": userchat,
				"text": message,
			})
		);
		chatSocket.send(
			JSON.stringify({
				"command": "send_notification",
				"sender_user": SenderUser,
				"receiver_user": userchat,
				"_type": "پیام متنی",
			})
		);
	  messageInputDom.value = "";
	};
}

if (document.querySelector("#click_inp") !=null){
	document.querySelector("#click_inp").onclick = function (e) {
		if (document.querySelector("#inp") != null){
			document.querySelector("#inp").click();
		}
	};
}
	



const compressImage = async (file, { quality = 1, type = file.type }) => {
  // Get as image data
  const imageBitmap = await createImageBitmap(file);

  // Draw to canvas
  const canvas = document.createElement('canvas');
  canvas.width = imageBitmap.width;
  canvas.height = imageBitmap.height;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(imageBitmap, 0, 0);

  // Turn into Blob
  const blob = await new Promise((resolve) =>
      canvas.toBlob(resolve, type, quality)
  );

  // Turn Blob into File
  return new File([blob], file.name, {
      type: blob.type,
  });
};

// Get the selected file from the file input
const input = document.querySelector('#inp');
if (input != null){
	input.addEventListener('change', async (e) => {
	  // Get the files
	  const { files } = e.target;

	  // No files selected
	  if (!files.length) return;

	  // We'll store the files in this data transfer object
	  const dataTransfer = new DataTransfer();

	  // For every file in the files list
	  for (const file of files) {
		  // We don't have to compress files that aren't images
		  if (!file.type.startsWith('image')) {
			  // Ignore this file, but do add it to our result
			  dataTransfer.items.add(file);
			  continue;
		  }

		  // We compress the file by 50%
		  const compressedFile = await compressImage(file, {
			  quality: 0.5,
			  type: 'image/jpeg',
		  });

		  // Save back the compressed file instead of the original file
		  dataTransfer.items.add(compressedFile);
	  }

	  // Set value of the file input to our new files list
	  e.target.files = dataTransfer.files;
	  if (e.target.files && e.target.files[0]) {
		var FR = new FileReader();
		FR.addEventListener("load", function(e) {
			chatSocket.send(JSON.stringify({
				"command": "send_image", 
				"text" : e.target.result,
				"from_user_username": SenderUser,
				"sender_chat_username": userchat,
			}));
			chatSocket.send(JSON.stringify({
				"command": "send_notification", 
				"sender_user": SenderUser,
				"_type": "پیام تصویری",
				"receiver_user": userchat,
			}));
		});
		FR.readAsDataURL(e.target.files[0])
	  }
	});
}

function op_new_tab(e) {
  var image = new Image();
  image.src = e.src
  var w = window.open("");
  w.document.write(image.outerHTML);
}


// create and show the notification
const showNotification = (text, link) => {
    // create a new notification
    const notification = new Notification(text, {
        body: link,
        vibrate: true
    });

    // navigate to a URL
    notification.addEventListener('click', () => {
        window.open(link, '_blank');
    });
}

// show an error message
const showError = () => {
	const error = document.querySelector('#show_error');
	error.style.display = 'block';
}

// show an error message
const hideError = () => {
	const error = document.querySelector('#show_error');
	if (error != null)
		error.style.display = 'none';
}

let granted = false;

if (Notification.permission === 'granted') {
    granted = true;
	hideError();
} else if (Notification.permission !== 'denied') {
    let permission = Notification.requestPermission();
    granted = permission === 'granted' ? true : false;
}

chatSocket.onmessage = function (e) {
	const data = JSON.parse(e.data)["message"];
	let is_after = false;
	let re = $("#my_username").val();
	if (data["command"] === "send_notification") {
		let sender_user = data["sender_user"];
		let _type = data["_type"];
		let link_chat = "";
		let text = "شما یک پیام " + _type + " از کاربر " + sender_user + " دارید";
		if(SenderUser != sender_user){
			// show notification or the error message 
			granted ? (showNotification(text, link_chat), hideError()) : showError();
		}
	}
	if (data["command"] === "fetch_message") {
		is_after = true;
		if (data["request_user"] === SenderUser) {
			createMessage(data, is_after);
			$("#conversation").animate({scrollTop: 0,},0);
		}
	} else if(data["command"] === "new_message") {
		createMessage(data, is_after);
		if (data["receiver_user"] == re) {
			$("#conversation").animate({scrollTop: 9999999999,},1400);
		}
	} else if(data["command"] === "send_image") {
	createMessage(data, is_after);
		if (data["receiver_user"] == re) {
			$("#conversation").animate({scrollTop: 9999999999,},1400);
		}
	}
};


function createMessage(data, is_after) {
  var chat_username = userchat;
  var sender_user = data["sender_user"];
  var receiver_user = data["receiver_user"];
  var text = data["text"];
  var image = data["image"];
  var date = data["date"];
  var is_received = data["is_received"];
  var is_read = data["is_read"];
  var el = '<div class="row message-body">';
  if (chat_username === sender_user) {
    el += '<div class="col-sm-12 message-main-receiver">';
    el += '<div class="receiver">';
  } else {
    el += '<div class="col-sm-12 message-main-sender">';
    el += '<div class="sender">';
  }
  
  if(image != null)
	el += '<img onclick="op_new_tab(this);" style="cursor: pointer;" class="op-new-tab" withd="50px" height="50px" src="' + image + '" alt="'+ chat_username + '">'
  if(text != null){
	  el += '<div dir="rtl" class="message-text">';
	  el += '<p style="white-space: pre-wrap;">';
	  el += text;
	  el += "</p>";
  }


  el += '<span class="message-time pull-right">';
  el += date;
  if (is_received) {
    el += '<i class="fa fa-check message-check" aria-hidden="true"></i>';
  }
  if (is_read) {
    el += '<i class="fa fa-check message-check" aria-hidden="true"></i>';
  }
  el += "</span>";
  el += "</div>";
  el += "</div>";
  el += "</div>";
  if (chat_username == receiver_user){
	  if (is_after) {
			$("#get_message").after(el);
	  } else {
			$("#conversation").append(el);
	  }
  }
  else if (chat_username == sender_user){
	  if (is_after) {
			$("#get_message").after(el);
	  } else {
			$("#conversation").append(el);
	  }
  }
}
