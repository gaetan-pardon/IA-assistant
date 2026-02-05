const baseURL = 'http://localhost:8000'

/**
 * Fetches the history of interactions for the logged-in user.
 * @returns response data
 */
export async function fetchHistory() {
    try {
        const response = await fetch(`${baseURL}/history`, {
            method: 'GET',
            credentials: "include"
        });
        const returned_response = await response.json();
        return returned_response;
    } catch (error) {
        console.error('Error fetching history:', error);
        throw error;
    }
}

export async function createHistory() {
    try {
        const response = await fetch(`${baseURL}/history`, {
            method: 'POST',
            credentials: "include"
        });
        const returned_response = await response.json();
        return returned_response;
    } catch (error) {
        console.error('Error creating history:', error);
        throw error;
    }
}

export async function addMessageToHistory(history_id, content) {
    try {
        const body = JSON.stringify({ message: content });
        console.log('Adding message to history with id:', history_id);
        console.log('Message content:', content);
        console.log('Request body:', body);
        const response = await fetch(`${baseURL}/history/${history_id}/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: "include",
            body: body
        });
        if (!response.ok) {
            console.log(response);
        }
        const returned_response = await response.json();
        return returned_response;
    } catch (error) {
        console.error('Error adding message to history:', error);
        throw error;
    }
}