import Container from '@mui/material/Container'
import Box from '@mui/material/Box'
import { ThemeProvider, createTheme, responsiveFontSizes } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import {
  Route,
  Routes 
} from 'react-router-dom'

import Header from './components/Header'

import Login from './pages/Login'
import Register from './pages/Register'
import Logout from './pages/Logout'

import CreateContact from './pages/CreateContact'

let theme = createTheme({
  palette: {
    mode: "dark",
    primary : {
      main: '#5061BC'
    }
  }
})

theme = responsiveFontSizes(theme)

function App() {
  return (
    <div>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Header />
        <Box mt={3}>
          <Container maxWidth="md">
            <Routes>
              <Route path="/login" element={<Login />}/>
              <Route path="/register" element={<Register />} />
              <Route path="/logout" element={<Logout />} />
              <Route path="/create/contact" element={<CreateContact />} />
            </Routes>
          </Container>
        </Box>
      </ThemeProvider>
    </div>
  );
}

export default App;
