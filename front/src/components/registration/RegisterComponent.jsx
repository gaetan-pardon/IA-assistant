import { useState } from "react";
import { registerUser } from "../../services/UserService";
import "./RegisterComponent.css"


export function RegistrationForm() {
    const [error, setError] = useState(null);


    async function handleSubmit() {
        const form = document.getElementById('registration-form');
        const email = form.elements['email'].value;
        const password = form.elements['password'].value;
        const confirmedPassword = form.elements['confirmed_password'].value;

        if (password != confirmedPassword)
        {
            setError("Passwords do not match");
            return;
        }

        const response = await registerUser(email, password);
        if (response.status !== 201) {
            setError(response.details || "Registration failed");
        } else {
            setError(null);
        }
    }


    return (
        <form className="registration-form" onSubmit={async (e) => { e.preventDefault(); handleSubmit(); }}>
            <label>Email</label>
            <input type='email' name="email" placeholder="Enter your email"/>
            <label>Password</label>
            <input type='password' name="password" placeholder="Enter your password"/>
            <label>Confirm your password</label>
            <input type='password' name="confirmed_password" placeholder="Confirm your password"/>
            <button type="submit">Create account</button>
            <div>{error}</div>
        </form>
    )
}