import { useState } from "react";
import { Link, useNavigate } from "react-router-dom"
import { registerUser } from "../../services/UserService";
import "./forms.css"



export function RegistrationForm() {
    const [error, setError] = useState(null);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmedPassword, setConfirmedPassword] = useState("");
    const navigate = useNavigate();


    async function handleSubmit(e) {
        e.preventDefault();

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
                navigate("/login");
                return;
            }
        } catch (error) {
            setError(error.message || "Network error");
        }
    }


    return (
        <section>
            <form className="connection-form" onSubmit={handleSubmit}>
                <label>Email</label>
                <input 
                    type='email' 
                    name="email" 
                    placeholder="Enter your email" 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required 
                />
                <label>Password</label>
                <input 
                    type='password' 
                    name="password" 
                    placeholder="Enter your password" 
                    pattern=".{8,72}" 
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required 
                    title="Your password must be at least 8 characters long and at most 72."
                />
                <label>Confirm your password</label>
                <input 
                    type='password' 
                    name="confirmed_password" 
                    placeholder="Confirm your password" 
                    pattern=".{8,72}" 
                    value={confirmedPassword}
                    onChange={(e) => setConfirmedPassword(e.target.value)}
                    required 
                    title="Your password must be at least 8 characters long and at most 72." 
                />
                <button type="submit">Create account</button>
                <div>Already have an account? Click <Link to="/login">here</Link></div>
            </form>
            <div className="error">{error}</div>
        </section>
    )
}