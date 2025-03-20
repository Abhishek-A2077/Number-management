import { useEffect, useContext } from 'react';
import { NumbersContext } from '../contexts/NumbersContext';
import { fetchNumbers } from '../services/api';
import NumberWindow from '../components/NumberWindow';
import StatsCard from '../components/StatsCard';
import NumberTypeSelector from '../components/NumberTypeSelector';

const Dashboard = () => {
  const { numbers, avg, numberType, updateWindow } = useContext(NumbersContext);

  useEffect(() => {
    const loadNumbers = async () => {
      const newNumbers = await fetchNumbers(numberType);
      updateWindow(newNumbers);
    };
    const interval = setInterval(loadNumbers, 5000);
    return () => clearInterval(interval);
  }, [numberType, updateWindow]);

  return (
    <div className="dashboard">
      <header>
        <h1>Number Management System</h1>
        <NumberTypeSelector />
      </header>
      
      <div className="grid">
        <StatsCard title="Current Average" value={avg.toFixed(2)} />
        <NumberWindow numbers={numbers} />
      </div>
    </div>
  );
};
