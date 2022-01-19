import React, { Fragment } from 'react'
import {
  Select,
  FormControl,
  Button,
  Dialog,
  DialogActions,
  DialogTitle,
  InputLabel,
  MenuItem,
  Box,
  TextField,
  Container,
  CssBaseline
} from '@mui/material'
import AddIcon from '@mui/icons-material/Add';
import api from '../axios'

export default class CreateEmail extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      contactID: props.contactID,
      open: false,
      email_type: '',
      email: ''
    }
  }

  handleToggle = () => {
    this.setState({
      open: !this.state.open
    })
  }

  handleSubmit = (e) => {
    e.preventDefault()
    api.post('/contacts/email', {
      contact: this.state.contactID,
      email_type: this.state.email_type,
      email: this.state.email
    })
    .then((res) => {
      if (res.status === 201){
        this.props.callbackData(res.data.id)
        this.setState({ open: false, email_type: '', email: '' })
      } else {
        // handle error
        console.log(res)
      }
    })
    .catch((err) => {
      console.log(err)
    })
  }

  render() {

    const { open } = this.state
    return (
      <Fragment>
        <Button onClick={this.handleToggle} color="success" variant="contained">
          Add <AddIcon />
        </Button>

        <Dialog
          open={open}
          keepMounted
          onClose={this.handleToggle}
          aria-describedby="alert-dialog-slide-description"
          sx={{
            minWidth: 25
          }}
        >
          <DialogTitle>{"Create new Email"}</DialogTitle>
            <Container component="main" maxWidth="md">
              <CssBaseline />
              <Box
                sx={{
                  marginTop: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                }}
              >
                <Box component="form" onSubmit={this.handleSubmit} noValidate mx={3} my={3}>
                  <FormControl fullWidth>
                    <InputLabel id="demo-simple-select-label">Email Type</InputLabel>
                    <Select
                      labelId="demo-simple-select-label"
                      id="demo-simple-select"
                      value={this.state.email_type}
                      label="Email Type"
                      onChange={(e) => this.setState({email_type: e.target.value})}
                    >
                      <MenuItem value="pers">Personal</MenuItem>
                      <MenuItem value="work">Work</MenuItem>
                    </Select>
                  </FormControl>
                  <TextField
                    margin="normal"
                    required
                    fullWidth
                    id="email"
                    label="Email"
                    name="email"
                    autoFocus
                    onChange={(e) => this.setState({email: e.target.value})}
                  />
                  <DialogActions sx={{ mt: 5 }}>
                    <Button onClick={this.handleToggle} variant="contained" color="error">Cancel</Button>
                    <Button type="submit" variant='contained' color="success">Create</Button>
                  </DialogActions>
                </Box>
              </Box>
            </Container>
        </Dialog>
      </Fragment>
    )
  }
}
