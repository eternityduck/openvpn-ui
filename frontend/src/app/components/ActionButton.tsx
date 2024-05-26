import React from 'react';
import styles from '../ActionButton.module.css';

interface ActionButtonProps {
    onClick: () => void;
    label: string;
    type: 'ratify' | 'revoke' | 'download';
}

const ActionButton: React.FC<ActionButtonProps> = ({ onClick, label, type }) => {
    return (
        <button
            className={`${styles.actionButton} ${
                type === 'ratify' ? styles.ratifyButton : type === 'revoke' ? styles.revokeButton : styles.downloadButton
            }`}
            onClick={onClick}
        >
            {label}
        </button>
    );
};

export default ActionButton;
