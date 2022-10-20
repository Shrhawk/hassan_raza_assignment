import { React, useEffect, useState } from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import { Spinner } from '../../components/spinner';
import TextField from '@mui/material/TextField';
import { authActions } from '../../../store/actions/auth.actions';
import labels from '../../../utils/labels';
import Grid from '@mui/material/Grid';
import { Alert } from '../../components/alert';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { TextareaAutosize } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

const theme = createTheme();

export default function MainPage(props) {
    const [age, setAge] = useState('');
    const [name, setName] = useState('');
    const [loading, setLoading] = useState(false);
    const [userDataLoading, setUserDataLoading] = useState(false);
    const [logoutLoading, setlogoutLoading] = useState(false);

    const profile = useSelector((state) => state.auth);
    const citiesList = useSelector((state) => state.auth.cities);

    const alert = useSelector((state) => state.alert);

    const [csvFile, setCsvFile] = useState();

    let navigate = useNavigate();

    const [gender, setGender] = useState('');
    const [country, setCountry] = useState('');
    const [city, setCity] = useState('');
    const [email, setEmail] = useState('');
    const [textValue, setTextValue] = useState('');
    const [inputText, setInputText] = useState('');
    const [countries, setCountries] = useState([]);
    const [newCities, setCitites] = useState([]);
    const [countryId, setCountryId] = useState();
    const [cityId, setCityId] = useState();
    const ageList = [];

    for (var i = 10; i < 100; i++) {
        ageList.push(i);
    }

    const dispatch = useDispatch();

    useEffect(() => {
        if (!profile?.loggedIn) {
            navigate('/');
        } else {
            dispatch(authActions.getProfile());
            dispatch(authActions.getCountries());
        }
    }, []);

    useEffect(() => {
        if (profile.userProfile?.name) {
            setName(profile.userProfile?.name);
            setAge(profile.userProfile?.age);
            setGender(profile.userProfile?.gender);
            setEmail(profile.userProfile?.email);
            setCityId(profile.userProfile?.city);
            setCountryId(profile.userProfile?.country);
        }
    }, [profile.userProfile?.name]);

    useEffect(() => {
        if (countries?.length && countryId) {
            let countryData = countries.find((item) => item.id === countryId);
            dispatch(authActions.getCities(countryData?.id));
            if (countryData) setCountry(countryData.name);
        }
    }, [countries, countryId]);

    useEffect(() => {
        if (citiesList?.length && cityId) {
            let cityData = citiesList.find((item) => item.id === cityId);
            if (cityData) setCity(cityData.name);
        }
    }, [citiesList, cityId]);

    useEffect(() => {
        if (profile.countries) {
            setCountries(profile.countries);
        }
    }, [profile.countries]);

    useEffect(() => {
        if (profile.user?.success) {
            navigate('/');
        }
    }, [profile.user?.success]);

    useEffect(() => {
        if (profile.fileUploadsuccess?.success) {
            navigate('/userinfo');
        }
    }, [profile.fileUploadsuccess?.success]);

    useEffect(() => {
        if (citiesList) {
            setCitites(citiesList);
        }
    }, [citiesList]);

    const handleName = (e) => {
        setName(e.target.value);
    };

    const handleGender = (e) => {
        setGender(e.target.value);
    };

    const handleAge = (e) => {
        setAge(e.target.value);
    };

    const handleCity = (e) => {
        let cityData = newCities.find((city) => city.name === e.target.value);
        setCity(e.target.value);
        setCityId(cityData.id);
    };

    const handleCountry = (e) => {
        let countryData = countries.find(
            (country) => country.name === e.target.value
        );
        setCountry(e.target.value);
        setCountryId(countryData.id);
        dispatch(authActions.getCities(countryData.id));
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setCsvFile(file);
        let reader = new FileReader();

        reader.onload = (e) => {
            const file = e.target.result;
            setInputText(file);
        };

        reader.onerror = (e) => alert(e.target.error.name);
        reader.readAsText(file);
    };

    const handleSubmit = () => {
        const data = {
            name: name,
            gender: gender,
            age: age,
            email: email,
            country: countryId,
            city: cityId
        };
        setUserDataLoading(true);
        dispatch(authActions.uploadUserProfile(data)).then((res) => {
            setUserDataLoading(false);
        });
    };

    const handleLogout = () => {
        setlogoutLoading(true);
        dispatch(authActions.logout()).then((res) => {
            setlogoutLoading(false);
        });
    };

    const handleCsvData = (e) => {
        setTextValue(e.target.value);
    };

    const handleReset = () => {
        setTextValue('');
    };

    const handleUpload = () => {
        if (csvFile && textValue) {
            const formdata = new FormData();
            formdata.append('sale_data', csvFile, csvFile.name);
            setLoading(true);
            dispatch(authActions.uploadCSVFile(formdata)).then((res) => {
                setLoading(false);
            });
        }
    };

    return (
        <ThemeProvider theme={theme}>
            <Container component="main">
                <CssBaseline />

                <Box component="form" noValidate>
                    <Grid container
                    spacing={2}>
                        <Grid
                           sx={{ display: 'flex', justifyContent: 'end' }}
                           item xs={12}
                        >
                        <Grid
                            sx={{
                                marginRight: "15px"
                            }}
                        >
                            <Button
                                size="small"
                                variant="contained"
                                onClick={()=>(
                                    navigate('/userinfo')
                                )}
                            >
                                
                                {labels.viewData}
                            </Button>
                        </Grid>
                        <Grid
                        >
                            <Button
                                size="small"
                                onClick={handleLogout}
                                variant="contained"
                                color="error"
                            >
                                {logoutLoading && <Spinner />}
                                {labels.logOut}
                            </Button>
                        </Grid>
                        </Grid>

                        <Grid
                            item
                            md={12}
                            sx={{ display: 'flex', justifyContent: 'start' }}
                        >
                            <Typography fontWeight={'800'}>User</Typography>
                        </Grid>

                        <Grid item lg={6} md={4} sm={12} xs={12}>
                            <FormControl fullWidth>
                                <TextField
                                    required
                                    size="small"
                                    id="Name"
                                    label="Name"
                                    name="name"
                                    value={name}
                                    autoComplete="name"
                                    autoFocus
                                    onChange={handleName}
                                />
                            </FormControl>
                        </Grid>
                        <Grid item lg={6} md={4} sm={12} xs={12}>
                            <FormControl size="small" fullWidth>
                                <InputLabel id="demo-simple-select-label">
                                    {labels.gender}
                                </InputLabel>
                                <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    value={gender}
                                    label="Gender"
                                    onChange={handleGender}
                                >
                                    <MenuItem value={'Male'}>Male</MenuItem>
                                    <MenuItem value={'Female'}>Female</MenuItem>
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid item lg={6} md={4} sm={12} xs={12}>
                            <FormControl size="small" fullWidth>
                                <InputLabel id="demo-simple-select-label">
                                    {labels.age}
                                </InputLabel>
                                <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    value={age}
                                    label="Age"
                                    onChange={handleAge}
                                >
                                    {ageList.map((item, index) => (
                                        <MenuItem value={item} key={index}>
                                            {item}
                                        </MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid item lg={6} md={4} sm={12} xs={12}>
                            <FormControl fullWidth>
                                <TextField
                                    size="small"
                                    required
                                    id="email"
                                    label="Email Address"
                                    name="email"
                                    autoComplete="email"
                                    value={email}
                                />
                            </FormControl>
                        </Grid>
                        <Grid item lg={6} md={4} sm={12} xs={12}>
                            <FormControl size="small" fullWidth>
                                <InputLabel id="demo-simple-select-label">
                                    Country
                                </InputLabel>
                                <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    label="Country"
                                    value={country}
                                    onChange={handleCountry}
                                >
                                    {countries.map((item, index) => (
                                        <MenuItem value={item.name} key={index}>
                                            {item.name}
                                        </MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid item lg={6} md={4} sm={12} xs={12}>
                            <FormControl size="small" fullWidth>
                                <InputLabel id="demo-simple-select-label">
                                    City
                                </InputLabel>
                                <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    value={city}
                                    label="City"
                                    onChange={handleCity}
                                >
                                    {newCities.map((item, index) => (
                                        <MenuItem value={item.name} key={index}>
                                            {item.name}
                                        </MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                        </Grid>

                        <Grid item md={2}>
                            <Button
                                size="small"
                                onClick={handleSubmit}
                                fullWidth
                                variant="contained"
                                color="error"
                                sx={{ mt: 1, mb: 1, p: 1 }}
                            >
                                {userDataLoading && <Spinner />}
                                {labels.updatedata}
                            </Button>

                            {alert.message ===
                            'profile successfully updated' ? (
                                <Alert
                                    message={alert.message}
                                    type={alert.type}
                                />
                            ) : (
                                ''
                            )}
                        </Grid>
                        <Grid item md={10}></Grid>

                        <Grid
                            item
                            md={12}
                            sx={{ display: 'flex', justifyContent: 'start' }}
                        >
                            <Typography fontWeight={'800'}>
                                Input Data
                            </Typography>
                        </Grid>

                        <Grid item md={9} sm={12} xs={12}>
                            <FormControl fullWidth>
                                <TextField
                                    size="small"
                                    type={'file'}
                                    fullWidth
                                    id="csv"
                                    onChange={handleFileChange}
                                />
                            </FormControl>
                        </Grid>
                        <Grid item md={3} sm={12} xs={12}>
                            <Button
                                size="small"
                                onClick={() => {
                                    setTextValue(inputText);
                                }}
                                sx={{ p: 1 }}
                                fullWidth
                                variant="contained"
                            >
                                Upload File
                            </Button>
                        </Grid>
                        <Grid item md={12} sm={12} xs={12}>
                            <TextareaAutosize
                                maxRows={15}
                                aria-label="empty textarea"
                                placeholder="Empty"
                                value={textValue}
                                onChange={handleCsvData}
                                style={{
                                    width: '100%',
                                    height: '150px',
                                    resize: 'none'
                                }}
                            />
                        </Grid>
                        <Grid
                            item
                            md={12}
                            sx={{ display: 'flex', justifyContent: 'center' }}
                        >
                            <Grid item md={2} sx={{ mr: 2 }}>
                                <Button
                                    size="small"
                                    sx={{ p: 1 }}
                                    fullWidth
                                    variant="contained"
                                    onClick={handleUpload}
                                >
                                    {loading && <Spinner />}
                                    Upload
                                </Button>
                            </Grid>
                            <Grid item md={2}>
                                <Button
                                    size="small"
                                    sx={{ p: 1 }}
                                    fullWidth
                                    color="error"
                                    variant="contained"
                                    onClick={handleReset}
                                >
                                    Reset
                                </Button>
                            </Grid>
                        </Grid>
                    </Grid>
                </Box>
            </Container>
        </ThemeProvider>
    );
}
