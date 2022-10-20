import { React, useState, useEffect } from 'react';
import Button from '@mui/material/Button';
import labels from '../../../utils/labels';
import { authActions } from '../../../store/actions/auth.actions';
import TextField from '@mui/material/TextField';
import InputLabel from '@mui/material/InputLabel';
import { DataGrid } from '@mui/x-data-grid';
import { Spinner } from '../../components/spinner';
import { Grid } from '@mui/material';
import Box from '@mui/material/Box';
import { Typography } from '@mui/material';
import { Container } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useDispatch, useSelector } from 'react-redux';
import { MenuItem } from '@mui/material';
import { FormControl } from '@mui/material';
import { Select } from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend } from 'recharts';
import { useNavigate } from 'react-router-dom';

const theme = createTheme();

const columns = [
    { field: 'sale_date', headerName: 'Date', width: 100 },
    { field: 'product_name', headerName: 'Product Name', width: 130 },
    { field: 'sale_number', headerName: 'Sale ', width: 130 },
    {
        field: 'revenue',
        headerName: 'Revenue',
        width: 90
    }
];

function UserInfo() {
    const [age, setAge] = useState('');
    const [name, setName] = useState('');
    const [gender, setGender] = useState('');
    const [country, setCountry] = useState('');
    const [city, setCity] = useState('');
    const [loading, setLoading] = useState(false);
    const [email, setEmail] = useState('');
    const [orderby, setOrderBy] = useState('date');
    const [chart, setChart] = useState('no_of_sale');
    const [countryId, setCountryId] = useState('');
    const [cityId, setCityId] = useState('');

    const [saleList, setSaleList] = useState([]);
    const [graphData, setGraphData] = useState([]);

    let navigate = useNavigate();

    const profile = useSelector((state) => state.auth.userProfile);
    const user = useSelector((state) => state.auth.user);
    const isLoggedIn = useSelector((state) => state.auth.loggedIn);
    const citiesList = useSelector((state) => state.auth.cities);
    const countries = useSelector((state) => state.auth.countries);
    const userSaleList = useSelector((state) => state.auth.userSaleData);
    const userGraphList = useSelector((state) => state.auth.graphSaleData);

    const dispatch = useDispatch();

    useEffect(() => {
        if (!isLoggedIn) {
            navigate('/');
        } else {
            dispatch(authActions.getProfile());
            dispatch(authActions.getCountries());
            dispatch(authActions.getUserSale());
            dispatch(authActions.getSaleGraph());
        }
    }, []);

    useEffect(() => {
        setName(profile?.name);
        setAge(profile?.age);
        setGender(profile?.gender);
        setEmail(profile?.email);
        setCountryId(profile?.country);
        setCityId(profile?.city);
    }, [
        profile?.name,
        profile?.age,
        profile?.gender,
        profile?.email,
        profile?.country,
        profile?.city
    ]);

    useEffect(() => {
        if (countries?.length && countryId) {
            let countryData = countries.find((item) => item.id === countryId);
            dispatch(authActions.getCities(countryData?.id));
            setCountry(countryData.name);
        }
    }, [countries, countryId]);

    useEffect(() => {
        if (citiesList?.length && cityId) {
            let cityData = citiesList.find((item) => item.id === cityId);
            if (cityData) setCity(cityData.name);
        }
    }, [citiesList, cityId]);

    useEffect(() => {
        if (userSaleList) {
            setSaleList(userSaleList);
        }
    }, [userSaleList]);

    useEffect(() => {
        if (userGraphList) {
            setGraphData(userGraphList);
        }
    }, [userGraphList]);

    useEffect(() => {
        if (user?.success) {
            navigate('/');
        }
    }, [user?.success]);

    const handleLogout = () => {
        setLoading(true);
        dispatch(authActions.logout()).then((res) => {
            setLoading(false);
        });
    };

    const handleOrder = (e) => {
        setOrderBy(e.target.value);
    };

    const handleChart = (e) => {
        setChart(e.target.value);
    };

    return (
        <ThemeProvider theme={theme}>
            <Box component="form" noValidate>
                <Container component="main">
                    <Grid container spacing={3}>
                        <Grid
                            item
                            md={12}
                            sx={{ display: 'flex', justifyContent: 'end' }}
                        >
                            <Button
                                size="small"
                                onClick={handleLogout}
                                variant="contained"
                                color="error"
                            >
                                {loading && <Spinner />}
                                {labels.logOut}
                            </Button>
                        </Grid>
                        <Grid item md={12}>
                            <Typography fontWeight={'800'}>
                                Personal Information
                            </Typography>
                        </Grid>
                        <Grid
                            container
                            sx={{
                                display: 'flex',
                                justifyContent: 'space-between'
                            }}
                        >
                            <Grid item lg={5.5} md={5.5} sm={12} xs={12}>
                                <FormControl fullWidth>
                                    <TextField
                                        variant="standard"
                                        fullWidth
                                        id="Name"
                                        label="Name"
                                        name="name"
                                        value={name}
                                        autoComplete="name"
                                        autoFocus
                                    />
                                </FormControl>
                            </Grid>
                            <Grid item lg={5.5} md={5.5} sm={12} xs={12}>
                                <FormControl fullWidth>
                                    <TextField
                                        variant="standard"
                                        fullWidth
                                        id="Email"
                                        label="Email"
                                        name="email"
                                        value={email}
                                        autoFocus
                                    />
                                </FormControl>
                            </Grid>
                        </Grid>
                        <Grid
                            container
                            sx={{
                                display: 'flex',
                                justifyContent: 'space-between'
                            }}
                        >
                            <Grid item lg={5.5} md={5.5} sm={12} xs={12}>
                                <FormControl fullWidth>
                                    <TextField
                                        variant="standard"
                                        fullWidth
                                        id="Age"
                                        label="Age"
                                        name="age"
                                        value={age}
                                        autoFocus
                                    />
                                </FormControl>
                            </Grid>
                            <Grid item lg={5.5} md={5.5} sm={12} xs={12}>
                                <FormControl fullWidth>
                                    <TextField
                                        variant="standard"
                                        fullWidth
                                        id="Country"
                                        label="Country"
                                        name="country"
                                        value={country}
                                        autoFocus
                                    />
                                </FormControl>
                            </Grid>
                        </Grid>

                        <Grid
                            container
                            sx={{
                                display: 'flex',
                                justifyContent: 'space-between'
                            }}
                        >
                            <Grid item lg={5.5} md={5.5} sm={12} xs={12}>
                                <FormControl fullWidth>
                                    <TextField
                                        variant="standard"
                                        fullWidth
                                        id="Gender"
                                        label="Gender"
                                        name="gender"
                                        value={gender}
                                        autoFocus
                                    />
                                </FormControl>
                            </Grid>
                            <Grid item lg={5.5} md={5.5} sm={12} xs={12}>
                                <FormControl fullWidth>
                                    <TextField
                                        variant="standard"
                                        fullWidth
                                        id="City"
                                        label="City"
                                        name="city"
                                        value={city}
                                        autoFocus
                                    />
                                </FormControl>
                            </Grid>
                        </Grid>
                        <Grid item lg={6} md={6} sm={12} xs={12}>
                            <Grid container>
                                <Grid item lg={5.5} md={5.5} sm={12} xs={12}>
                                    <Typography fontWeight={'600'}>
                                        Data
                                    </Typography>
                                </Grid>
                                <Grid item lg={5.5} md={5.5} sm={12} xs={12}>
                                    <FormControl size="small" fullWidth>
                                        <InputLabel id="demo-simple-select-label">
                                            {'Order By'}
                                        </InputLabel>
                                        <Select
                                            labelId="demo-simple-select-label"
                                            id="demo-simple-select"
                                            label="Order by"
                                            value={orderby}
                                            onChange={handleOrder}
                                        >
                                            <MenuItem value={orderby}>
                                                Date
                                            </MenuItem>
                                        </Select>
                                    </FormControl>
                                </Grid>
                                <Grid item md={5.5} lg={11} sm={12} xs={12}>
                                    <Box
                                        sx={{
                                            height: 350,
                                            width: '100%',
                                            pt: 3
                                        }}
                                    >
                                        <DataGrid
                                            initialState={{
                                                sorting: {
                                                    sortModel: [
                                                        {
                                                            field: { orderby },
                                                            sort: 'desc'
                                                        }
                                                    ]
                                                }
                                            }}
                                            rows={saleList}
                                            columns={columns}
                                            pageSize={5}
                                            rowsPerPageOptions={[5]}
                                            checkboxSelection
                                            disableSelectionOnClick
                                            experimentalFeatures={{
                                                newEditingApi: true
                                            }}
                                        />
                                    </Box>
                                </Grid>
                            </Grid>
                        </Grid>
                        <Grid item lg={6} md={6} sm={12} xs={12}>
                            <Grid container>
                                <Grid item lg={6} md={6} sm={12} xs={12}>
                                    <Typography fontWeight={'600'}>
                                        Chart
                                    </Typography>
                                </Grid>
                                <Grid item lg={6} md={6} sm={12} xs={12}>
                                    <FormControl size="small" fullWidth>
                                        <InputLabel id="demo-simple-select-label">
                                            {'Y-axis'}
                                        </InputLabel>
                                        <Select
                                            labelId="demo-simple-select-label"
                                            id="demo-simple-select"
                                            value={chart}
                                            label="Chart"
                                            onChange={handleChart}
                                        >
                                            <MenuItem value={chart}>
                                                {' '}
                                                Sales Number
                                            </MenuItem>
                                        </Select>
                                    </FormControl>
                                </Grid>
                                <Grid item md={12} lg={12} sm={12} xs={12}>
                                    <Box
                                        sx={{ height: 400, width: 500, pt: 3 }}
                                    >
                                        <BarChart
                                            width={600}
                                            height={350}
                                            data={graphData}
                                            margin={{
                                                top: 5,
                                                right: 30,
                                                left: 20,
                                                bottom: 5
                                            }}
                                        >
                                            <CartesianGrid strokeDasharray="2 1" />

                                            <XAxis dataKey="product_name" />
                                            <YAxis />
                                            <Legend />
                                            <Bar
                                                dataKey="no_of_sale"
                                                fill="#1976d2"
                                            />
                                        </BarChart>
                                    </Box>
                                </Grid>
                            </Grid>
                        </Grid>
                    </Grid>
                </Container>
            </Box>
        </ThemeProvider>
    );
}
export default UserInfo;
