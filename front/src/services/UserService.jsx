const baseURL = 'http://localhost:8000'

/**
 * Registers a new user with the given email and password.
 * @param {*} email - user's email
 * @param {*} password - user's password
 * @returns response data
 */
export async function registerUser(email, password) {
    try {
        
        const response = await fetch(`${baseURL}/user/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "email": email, "password": password })
        });
        const data = await response.json();
        return { ...data, status: response.status };
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
        const response = await fetch(`${baseURL}/user/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: "include",
            body: JSON.stringify({ email, password })
        });
        const data = await response.json();
        return { ...data, status: response.status };
    } catch (error) {
        console.error('Error logging in user:', error);
        throw error;
    }
}

/**
 * Logs out the current user by deleting the access token cookie.
 * @returns response data
 */
export async function logoutUser() {
    try {
        const response = await fetch(`${baseURL}/user/logout`, {
            method: 'POST',
            credentials: "include"
        });
        if (response.status === 204) {
            return { success: true, message: "Logged out successfully" };
        }
        return await response.json();
    } catch (error) {
        console.error('Error logging out user:', error);
        throw error;
    }
}

/**
 * Verifies the user's token by making a request to a protected route.
 * @returns response data
 */
export async function verifyToken() {
    try {
        const response = await fetch(`${baseURL}/user/protected-route`, {
            method: 'GET',
            credentials: "include"
        });
        if (!response.ok) {
            throw new Error('Token verification failed');
        }
        const data = await response.json();
        return { data, status: response.status };
    } catch (error) {
        console.error('Error verifying token:', error);
        throw error;
    }
}