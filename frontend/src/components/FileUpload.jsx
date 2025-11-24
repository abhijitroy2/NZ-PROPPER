import React, { useState, useRef } from 'react';

const FileUpload = ({ onFileSelect, disabled }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(null);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleFileInput = (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleFile = (file) => {
    // Validate file type
    const validTypes = [
      'text/csv',
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    ];
    const validExtensions = ['.csv', '.xlsx', '.xls'];

    const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
    const isValidType = validTypes.includes(file.type) || validExtensions.includes(fileExtension);

    if (!isValidType) {
      alert('Please upload a CSV or Excel file (.csv, .xlsx, .xls)');
      return;
    }

    setUploadProgress('Processing...');
    onFileSelect(file);
    setUploadProgress(null);
  };

  const openFileDialog = () => {
    fileInputRef.current?.click();
  };

  return (
    <div style={{ marginBottom: '2rem' }}>
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={disabled ? null : openFileDialog}
        style={{
          border: `2px dashed ${isDragging ? '#4CAF50' : '#ccc'}`,
          borderRadius: '8px',
          padding: '3rem',
          textAlign: 'center',
          cursor: disabled ? 'not-allowed' : 'pointer',
          backgroundColor: isDragging ? '#f0f8f0' : '#fff',
          transition: 'all 0.3s ease',
          opacity: disabled ? 0.6 : 1,
        }}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={handleFileInput}
          style={{ display: 'none' }}
          disabled={disabled}
        />
        {uploadProgress ? (
          <p style={{ color: '#666', fontSize: '1.1rem' }}>{uploadProgress}</p>
        ) : (
          <>
            <p style={{ fontSize: '1.2rem', marginBottom: '0.5rem', color: '#333' }}>
              {isDragging ? 'Drop file here' : 'Click or drag file here to upload'}
            </p>
            <p style={{ color: '#666', fontSize: '0.9rem' }}>
              Supports CSV and Excel files (.csv, .xlsx, .xls)
            </p>
          </>
        )}
      </div>
    </div>
  );
};

export default FileUpload;


