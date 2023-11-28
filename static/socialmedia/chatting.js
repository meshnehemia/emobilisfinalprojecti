setInterval(() => {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/getmychats/individual/", true);
    xhr.onload = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                try {
                    const responseData = JSON.parse(xhr.responseText);
                    const chatList = responseData.mychats.map(chat => {
                        if (chat.user !== chat.sendername) {
                            return `
                                    <div class="roomListRoom">
                                        <div class="roomListRoom__header">
                                            <a href="/profile/${chat.senderid}/" class="roomListRoom__author">
                                                <div class="avatar avatar--small active">
                                                    <img src="${chat.sendericon}"/>
                                                </div>
                                                <span>@${chat.sendername}</span>
                                            </a>
                                            <div class="roomListRoom__actions">
                                                <span>${chat.time} ago</span>
                                            </div>
                                        </div>
                                        <div class="roomListRoom__content">
                                            <a href="/chatscreem/${chat.senderid}/">${chat.sendername}</a>
                                        </div>
                                    </div>`;
                        } else if (chat.user !== chat.receiver) {
                            return `
                                    <div class="roomListRoom">
                                        <div class="roomListRoom__header">
                                            <a href="/profile/${chat.receiverid}/" class="roomListRoom__author">
                                                <div class="avatar avatar--small active">
                                                    <img src="${chat.receivericon}"/>
                                                </div>
                                                <span>@${chat.receiver}</span>
                                            </a>
                                        </div>
                                        <div class="roomListRoom__content">
                                            <a href="/chatscreem/${chat.receiverid}/">${chat.receiver}</a>
                                        </div>
                                    </div>`;
                        }
                    }).join();
                    document.querySelector('.checking').innerHTML = chatList;
                    // Process the JSON data
                } catch (error) {
                    console.error("Error parsing JSON:", error);
                }
            } else {
                console.error("HTTP request failed with status:", xhr.status);
            }
        }
    };
    xhr.onerror = (error) => {
        console.error("Request failed:", error);
    };
    xhr.send();
}, 1000)
