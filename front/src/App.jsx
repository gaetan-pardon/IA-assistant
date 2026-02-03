import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import RegistrationPage from "./pages/register";

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/register" element={<RegistrationPage/>}/>
      </Routes>
    </Router>
  )
}

export default App