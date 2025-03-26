// filepath: c:\Users\Admin\Desktop\dashui-synapse-connector\static\script.test.js
const fetchMock = require('jest-fetch-mock');
fetchMock.enableMocks();

const { handleOption } = require('./script');

beforeEach(() => {
    fetch.resetMocks();
});

test('pull related incidents', async () => {
    document.body.innerHTML = `
        <div class="chatbox"></div>
        <textarea class="chat-input"></textarea>
    `;

    const chatbox = document.querySelector('.chatbox');
    const chatInput = document.querySelector('.chat-input');
    chatInput.value = 'INC0000060';

    fetch.mockResponseOnce(JSON.stringify({
        related_incidents: ['INC0000061', 'INC0000062']
    }));

    await handleOption('pull related incidents');

    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/incident/INC0000060/related', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });

    const incomingMessages = chatbox.querySelectorAll('.chat.incoming p');
    expect(incomingMessages.length).toBe(1);
    expect(incomingMessages[0].textContent).toContain('INC0000061');
    expect(incomingMessages[0].textContent).toContain('INC0000062');
});