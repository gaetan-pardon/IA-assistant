import "./login.css"
import { LoginForm } from "../../components/login/LoginComponent"

export default function LoginPage() {
    return (
        <div className="login-component">
            <h1>Log in</h1>
            <LoginForm/>
        </div>
    )
}