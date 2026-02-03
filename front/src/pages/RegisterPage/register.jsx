import { RegistrationForm } from "../../components/registration/RegisterComponent"
import "./register.css"

export default function RegistrationPage() {
    return (
        <div className="registration-component">
            <h1>Account Creation</h1>
            <RegistrationForm/>
        </div>
    )
}