const baseURL = 'http://localhost:8000'

/**
 * Registers a new user with the given email and password.
 * @param {*} email - user's email
 * @param {*} password - user's password
 * @returns response data
 */
export async function registerUser(email, password) {
    try {
        
        const response = await fetch(`${baseURL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "email": email, "password": password })
        });
        const returned_response = await response.json();
        console.log(returned_response)
        return returned_response;
    } catch (error) {
        console.error('Error registering user:', error);
        throw error;
    }
}

/**
 * Logs in a user with the given email and password.
 * @param {*} email - user's email
 * @param {*} password - user's password
 * @returns response data
 */
export async function loginUser(email, password) {
    try {
        const response = await fetch(`${baseURL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        console.log("response: " + response)
        return await response.json();
    } catch (error) {
        console.error('Error logging in user:', error);
        throw error;
    }
}