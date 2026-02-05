import './forms.css';

import { useState } from "react";
import { Link, useNavigate } from "react-router-dom"
import { loginUser } from "../../services/UserService";



export function LoginForm() {
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    async function handleSubmit() {
        const form = document.getElementById('login-form');
        const email = form.elements['email'].value;
        const password = form.elements['password'].value;

        try {
            const response = await loginUser(email, password);
            if (response.status === 200) {
                navigate("/chat");
            } else {
                setError(response.details || response.message || "Login failed");
            }
        } catch (error) {
            setError(error.message || "Network error");
        }
    }


    return (
        <section>
            <form id="login-form" className="connection-form" onSubmit={async (e) => { e.preventDefault(); handleSubmit(); }}>
                <label>Email</label>
                <input type='email' name="email" placeholder="Enter your email" required />
                <label>Password</label>
                <input type='password' name="password" placeholder="Enter your password" pattern=".{8,72}" required title="Your password must be at least 8 characters long and at most 72."/>
                <button type="submit">Log in</button>
                <div>Don't have an account? Click <Link to="/register">here</Link></div>
            </form>
            <div className="error">{error}</div>
        </section>
    )
}