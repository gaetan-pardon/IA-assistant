/**
 * Registers a new user with the given email and password.
 * @param {*} email - user's email
 * @param {*} password - user's password
 * @returns response data
 */
export async function registerUser(email, password) {
    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
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