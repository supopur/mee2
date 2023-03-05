const form = document.querySelector("form");
const tokenInput = form.querySelector("#token");
const nameInput = form.querySelector("#name");
const statusSelect = form.querySelector("#status");

// set the token input as password field
tokenInput.setAttribute("type", "password");

// function to get the config values from the server
const getConfigValues = async () => {
    try {
        const tokenResponse = await fetch('/api/token');
        const tokenValue = await tokenResponse.text();
        tokenInput.value = tokenValue;

        const nameResponse = await fetch('/api/name');
        const nameValue = await nameResponse.text();
        nameInput.value = nameValue;

        const statusResponse = await fetch('/api/status');
        const statusValue = await statusResponse.text();
        statusSelect.value = statusValue;
    } catch (error) {
        console.error(error);
    }
}

getConfigValues();

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const token = tokenInput.value;
    const name = nameInput.value;
    const status = statusSelect.value;

    try {
        // send POST request to /api/token endpoint with token as the body
        if (token !== '') {
            await fetch('/api/token', {
                method: 'POST',
                body: token
            });
        }


        // send POST request to /api/name endpoint with name as the body
        if (name !== '') {
            await fetch('/api/name', {
                method: 'POST',
                body: name
            });
        }


        // send POST request to /api/status endpoint with status as the body
        if (status !== '') {
            await fetch('/api/status', {
                method: 'POST',
                body: status
            });
        }

    } catch (error) {
        console.error(error);
    }
});