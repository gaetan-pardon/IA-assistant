import { useState } from "react";
import { Link } from "react-router-dom"
import { registerUser } from "../../services/UserService";
import "./forms.css"



export function RegistrationForm() {
    const [error, setError] = useState(null);


    async function handleSubmit() {
        const form = document.getElementById('registration-form');
        const email = form.elements['email'].value;
        const password = form.elements['password'].value;
        const confirmedPassword = form.elements['confirmed_password'].value;

        if (password !== confirmedPassword)
        {
            setError("Passwords do not match");
            return;
        }

        try {
            const response = await registerUser(email, password);
            if (response.status !== 201) {
                setError(response.details || "Registration failed");
                return;
            } else {
                setError(response.message);
                return;
            }
        } catch (error) {
            setError(error.message || "Network error");
        }
    }


    return (
        <section>
            <form id="registration-form" className="connection-form" onSubmit={async (e) => { e.preventDefault(); handleSubmit(); }}>
                <label>Email</label>
                <input type='email' name="email" placeholder="Enter your email" required />
                <label>Password</label>
                <input type='password' name="password" placeholder="Enter your password" pattern=".{8,72}" required title="Your password must be at least 8 characters long and at most 72."/>
                <label>Confirm your password</label>
                <input type='password' name="confirmed_password" placeholder="Confirm your password" pattern=".{8,72}" required title="Your password must be at least 8 characters long and at most 72." />
                <button type="submit">Create account</button>
                <div>Already have an account? Click <Link to="/login">here</Link></div>
            </form>
            <div className="error">{error}</div>
        </section>
    )
}