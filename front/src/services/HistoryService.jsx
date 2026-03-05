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
        if (!response.ok) {
            throw new Error(`Failed to fetch history: ${response.status}`);
        }
        const data = await response.json();
        return { data, status: response.status };
    } catch (error) {
        console.error('Error fetching history:', error);
        throw error;
    }
}

/**
 * Fetches a specific history by its ID.
 * @param {*} history_id 
 * @returns 
 */
export async function fetchHistoryById(history_id) {
    try {
        const response = await fetch(`${baseURL}/history/${history_id}`, {
            method: 'GET',
            credentials: "include"
        });
        if (!response.ok) {
            throw new Error(`Failed to fetch history by ID: ${response.status}`);
        }
        const data = await response.json();
        return { data, status: response.status };
    } catch (error) {
        console.error('Error fetching history by ID:', error);
        throw error;
    }
}

/**
 * Creates a new history for the logged-in user.
 * @returns response data
 */
export async function createHistory() {
    try {
        const response = await fetch(`${baseURL}/history`, {
            method: 'POST',
            credentials: "include"
        });
        if (!response.ok) {
            throw new Error(`Failed to create history: ${response.status}`);
        }
        const data = await response.json();
        return { data, status: response.status };
    } catch (error) {
        console.error('Error creating history:', error);
        throw error;
    }
}

/**
 * Adds a message to a specific history.
 * @param {*} history_id 
 * @param {*} content 
 * @returns response data
 */
export async function addMessageToHistory(history_id, content) {
    try {
        const body = JSON.stringify({ message: content });
        const response = await fetch(`${baseURL}/history/${history_id}/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: "include",
            body: body
        });
        if (!response.ok) {
            throw new Error(`Failed to add message: ${response.status}`);
        }
        const data = await response.json();
        return { data, status: response.status };
    } catch (error) {
        console.error('Error adding message to history:', error);
        throw error;
    }
}

/**
 * Deletes a specific history by its ID.
 * @param {*} history_id 
 * @returns response data
 */
export async function deleteHistoryService(history_id) {
    try {
        const response = await fetch(`${baseURL}/history/${history_id}`, {
            method: 'DELETE',
            credentials: "include"
        });
        if (!response.ok) {
            throw new Error(`Failed to delete history: ${response.status}`);
        }
        const data = await response.json();
        return { data, status: response.status };
    } catch (error) {
        console.error('Error deleting history:', error);
        throw error;
    };
}