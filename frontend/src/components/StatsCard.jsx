import { useContext } from 'react';
import { NumbersContext } from '../contexts/NumbersContext';

const StatsCard = ({ title }) => {
  const { avg } = useContext(NumbersContext);

  return (
    <div className="stats-card">
      <h3>{title}</h3>
      <div className="value">{avg.toFixed(2)}</div>
      <div className="trend">
        <span className="material-icons">📈</span>
        <span>Last 10 numbers average</span>
      </div>
    </div>
  );
};
