import { default as React, useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { authActions } from '../../../store/actions/auth.actions';
import labels from '../../../utils/labels';
import { Alert } from '../../components/alert/alert';
import { Spinner } from '../../components/spinner';
import { useNavigate } from 'react-router-dom';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';

export function Home() {
    let navigate = useNavigate();

    const [userInputs, setUserInputs] = useState({
        email: '',
        password: ''
    });

    const [loading, setLoading] = useState(false);
    const [emailError, setEmailError] = useState('');
    const [passwordError, setPasswordError] = useState('');
    const alert = useSelector((state) => state.alert);
    const loggedIn = useSelector((state) => state.auth);
    const { email, password } = userInputs;
    const dispatch = useDispatch();

    useEffect(() => {
        if (loggedIn?.user?.access_token) {
            navigate('/mainpage');
        }
    }, [loggedIn?.user?.access_token]);

    useEffect(() => {
        if (loggedIn?.userProfile?.name) {
            navigate('/mainpage');
        }
    }, []);

    function handleChange(e) {
        const { name, value } = e.target;
        setUserInputs((inputs) => ({ ...inputs, [name]: value }));
    }

    function handleSubmit(e) {
        e.preventDefault();
        if (validateEmail() && validatePassword()) {
            setLoading(true);
            dispatch(authActions.login(email, password)).then((res) => {
                setLoading(false);
            });
        }
    }

    const validateEmail = () => {
        let input = userInputs;
        let isValid = true;

        if (!input['email']) {
            isValid = false;
            setEmailError('Field cannot be empty.');
        } else if (typeof input['email'] !== 'undefined') {
            var pattern = new RegExp(
                /^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i
            );
            if (!pattern.test(input['email'])) {
                isValid = false;
                setEmailError('Email must be valid.');
            } else {
                setEmailError('');
            }
        } else {
            setEmailError('');
        }
        return isValid;
    };

    const validatePassword = () => {
        let input = userInputs;
        let isValid = true;

        if (!input['password']) {
            isValid = false;
            setPasswordError('Password missing.');
        } else {
            setPasswordError('');
        }
        return isValid;
    };

    const theme = createTheme();

    return (
        <ThemeProvider theme={theme}>
            <Container component="main" maxWidth="xs">
                <CssBaseline />
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center'
                    }}
                >
                    <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                        <LockOutlinedIcon />
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Sign in
                    </Typography>
                    <Box
                        component="form"
                        onSubmit={handleSubmit}
                        noValidate
                        sx={{ mt: 1 }}
                    >
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="email"
                            label="Email Address"
                            name="email"
                            autoComplete="email"
                            autoFocus
                            onChange={handleChange}
                            onBlur={() => {
                                validatePassword();
                            }}
                            helperText={emailError}
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                            onChange={handleChange}
                            onBlur={() => {
                                validatePassword();
                            }}
                        />

                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            {loading && <Spinner />}
                            {labels.login}
                        </Button>
                        {alert.message ? (
                            <Alert message={alert.message} type={alert.type} />
                        ) : (
                            ''
                        )}
                    </Box>
                </Box>
            </Container>
        </ThemeProvider>
    );
}
