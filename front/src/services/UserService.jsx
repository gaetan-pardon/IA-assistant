const baseURL = 'http://localhost:8000'

/**
 * Registers a new user with the given email and password.
 * @param {*} email - user's email
 * @param {*} password - user's password
 * @returns response data
 */
export async function registerUser(email, password) {
    try {
        
        console.log(JSON.stringify({ "email": email, "password": password }));
        const response = await fetch(`${baseURL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "email": email, "password": password })
        });

        return await response.json();
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
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.details || 'Login failed');
        }

        return await response.json();
    } catch (error) {
        console.error('Error logging in user:', error);
        throw error;
    }
}