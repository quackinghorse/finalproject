import React, { useState, useEffect } from 'react';
import {
    Box, Container, Typography, Paper, AppBar, Toolbar, CssBaseline
} from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { styled } from '@mui/system';
import MenuIcon from '@mui/icons-material/Menu';
import Webcam from 'react-webcam';
import { MapContainer, TileLayer, Marker, Circle, useMap, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import axios from 'axios';

// Import the custom marker image
import customMarkerImage from './marker.jpeg';  // Make sure the path is correct relative to your component file

const theme = createTheme({
    palette: {
        primary: { main: '#0d47a1' },
        secondary: { main: '#ff5722' },
        background: { default: '#f5f5f5' },
    },
    typography: {
        h4: { fontWeight: 600 },
        subtitle1: { color: '#757575' },
    },
});

const PageContainer = styled(Box)({
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gridTemplateRows: 'repeat(2, auto) 1fr auto',
    gap: theme.spacing(2),
    padding: theme.spacing(2),
});

const CameraFeedContainer = styled(Paper)(({ theme }) => ({
    padding: theme.spacing(3),
    textAlign: 'center',
    borderRadius: theme.shape.borderRadius,
    boxShadow: theme.shadows[3],
}));

const MapContainerStyled = styled(Box)({
    height: '50vh',
    gridColumn: '1 / -1',
    borderRadius: theme.shape.borderRadius,
    overflow: 'hidden',
    boxShadow: theme.shadows[3],
});

const DataContainer = styled(Paper)(({ theme }) => ({
    padding: theme.spacing(2),
    gridColumn: '1 / -1',
    borderRadius: theme.shape.borderRadius,
    boxShadow: theme.shadows[3],
}));

const GasSensorContainer = styled(Box)(({ theme }) => ({
    position: 'fixed',
    top: theme.spacing(2),
    right: theme.spacing(2),
    padding: theme.spacing(2),
    backgroundColor: theme.palette.primary.main,
    color: '#fff',
    borderRadius: theme.shape.borderRadius,
    boxShadow: theme.shadows[5],
    zIndex: 1000,
}));

// Create a custom marker icon using the imported image
const customMarkerIcon = new L.Icon({
    iconUrl: customMarkerImage,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
});

const MapEventsHandler = ({ setCurrentMarker, setMarkerPosition }) => {
    const map = useMap();

    useMapEvents({
        click: (e) => {
            const { lat, lng } = e.latlng;
            setCurrentMarker([lat, lng]);

            axios.post('/api/post-coordinates/', {
                latitude: lat,
                longitude: lng,
            })
            .then(response => {
                if (response.status === 200) {
                    console.log('Coordinates sent successfully.');
                } else {
                    console.error('Error sending coordinates. Status:', response.status);
                }
            })
            .catch(error => {
                console.error('Error sending coordinates:', error);
            });

            map.setView([lat, lng], map.getZoom());
        }
    });

    return null;
};

const App = () => {
    const [gasValue, setGasValue] = useState(null);
    const [markerPosition, setMarkerPosition] = useState({ lat: 30.35515908622681 , lng: 76.36968580268332 });
    const [currentMarker, setCurrentMarker] = useState(null);
    const [detections, setDetections] = useState([]);
    const [accuracy, setAccuracy] = useState(100);

    const fetchGasSensorValue = () => {
        axios.get('http://127.0.0.1:8000/api/get-gas-sensor-value/')
            .then(response => setGasValue(response.data.gas_value))
            .catch(error => console.error('Error fetching gas sensor value:', error));
    };

    const fetchDetections = () => {
        axios.get('http://127.0.0.1:8000/api/get-detection/')
            .then(response => setDetections(response.data.detections || []))
            .catch(error => console.error('Error fetching detections:', error));
    };

    useEffect(() => {
        fetchGasSensorValue();
        const gasSensorInterval = setInterval(fetchGasSensorValue, 5000);

        fetchDetections();
        const detectionsInterval = setInterval(fetchDetections, 5000);

        return () => {
            clearInterval(gasSensorInterval);
            clearInterval(detectionsInterval);
        };
    }, []);

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <AppBar position="static">
                <Toolbar>
                    <MenuIcon edge="start" color="inherit" aria-label="menu" />
                    <Typography variant="h6">
                        Disaster Management Robot Monitoring
                    </Typography>
                </Toolbar>
            </AppBar>

            <GasSensorContainer>
                <Typography variant="h6">Gas Sensor Status</Typography>
                <Typography variant="subtitle1">
                    {gasValue ? `Smoke Detected: ${gasValue}` : 'Smoke Not Detected'}
                </Typography>
            </GasSensorContainer>

            <Container>
                <PageContainer>
                    <CameraFeedContainer>
                        <Typography variant="h4">Thermal Camera Feed</Typography>
                        <Typography variant="subtitle1">Monitor the thermal feed from the robot</Typography>
                        <Webcam videoConstraints={{ deviceId: "thermal-camera-id" }} />
                    </CameraFeedContainer>

                    <CameraFeedContainer>
                        <Typography variant="h4">Normal Camera Feed</Typography>
                        <Typography variant="subtitle1">Monitor the normal camera feed from the robot</Typography>
                        <Webcam videoConstraints={{ deviceId: "normal-camera-id" }} />
                    </CameraFeedContainer>

                    <MapContainerStyled>
                        <MapContainer center={[markerPosition.lat, markerPosition.lng]} zoom={13} style={{ height: '100%', width: '100%' }}>
                            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                            {markerPosition && (
                                <>
                                    {/* <Marker position={markerPosition} icon={customMarkerIcon} /> */}
                                    <Circle center={markerPosition} radius={accuracy} color="red" />
                                </>
                            )}
                            {currentMarker && (
                                <Marker position={currentMarker} icon={customMarkerIcon} />
                            )}
                            <MapEventsHandler setCurrentMarker={setCurrentMarker} setMarkerPosition={setMarkerPosition} />
                        </MapContainer>
                    </MapContainerStyled>

                    <DataContainer>
                        <Typography variant="h4">Gas and Sensor Data</Typography>
                        <Typography variant="subtitle1">Review the collected gas and sensor data</Typography>
                        <Typography variant="body1">Gas Value: {gasValue}</Typography>
                    </DataContainer>
                </PageContainer>
            </Container>
        </ThemeProvider>
    );
};

export default App;
