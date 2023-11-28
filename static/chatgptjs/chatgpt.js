const messagesList = document.querySelector('.messages-list');
const messageForm = document.querySelector('.message-form');
const messageInput = document.querySelector('.message-input');
let mymessage = "";
messageForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const message = messageInput.value.trim();
    if (message.length === 0) {
        return;
    } else {
        mymessage += "me : " + message + " .";
        const messageItem = document.createElement('li');
        messageItem.classList.add('message', 'sent');
        messageItem.innerHTML = `
                     <div class="d-flex justify-content-end">
                                    <div class="d-flex flex-row justify-content-end mb-4 pt-1"><div>
                                        <p class="small p-2 me-3 mb-3 text-dark bg-white rounded-3 bg-warning" style="margin-left: 70px;margin-top: 50px;">${message}</p>
                                    </div>
                                        <div class="d-block">
                                            <p class="small">You</p>
                                            <img src=${profile} alt="avatar 1" style="width: 45px; height: 45px; margin-top:-14px; margin-right: 10px;border-radius: 50% ">
                                        </div>
                                    </div>
                                </div>`;
        messagesList.appendChild(messageItem);
        messageInput.value = '';
        fetch('', {
            method: 'POST',
            header: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: new URLSearchParams({
                'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'message': mymessage
            })
        })
            .then(response => response.json())
            .then(data => {
                const response = data.response;
                const messageItem = document.createElement('li');
                messageItem.classList.add('message', 'received');
                mymessage += " assistance AI : " + response + " .";
                messageItem.innerHTML = `
                            <div class="messages-list">
                                <div class="d-flex justify-content-start">
                                   <div class="d-block">
                                            <p class="small">CHATBOT</p>
                                            <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava6-bg.webp" alt="avatar 1" style="width: 45px; height: 45px; margin-top:-17px; margin-right: 10px ">
                                   </div>

                                    <p class="bg-white p-2 rounded " style="margin-right: 70px ;margin-top: 50px">${response}</p>
                                </div>

                            </div>
                        </div>
                        `;
                console.log(mymessage)
                messagesList.appendChild(messageItem);
            })
    }
})

