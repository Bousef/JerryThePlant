-- PlantAI Supabase Database Schema
-- Run these SQL commands in your Supabase SQL Editor

-- Create sensor_readings table
CREATE TABLE IF NOT EXISTS sensor_readings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    temperature DECIMAL(5,2) NOT NULL,
    pressure DECIMAL(7,2) NOT NULL,
    humidity DECIMAL(5,2) NOT NULL,
    soil_moisture DECIMAL(5,2) NOT NULL,
    ai_reply TEXT,
    status_color VARCHAR(10) CHECK (status_color IN ('green', 'yellow', 'red')),
    source VARCHAR(50) DEFAULT 'raspberry_pi',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create plant_images table
CREATE TABLE IF NOT EXISTS plant_images (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    original_filename VARCHAR(255) NOT NULL,
    stored_filename VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    image_url TEXT NOT NULL,
    storage_type VARCHAR(20) DEFAULT 'supabase',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create metrics table
CREATE TABLE IF NOT EXISTS plant_metrics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    metrics JSONB NOT NULL,
    source VARCHAR(50) DEFAULT 'api_request',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_sensor_readings_created_at ON sensor_readings(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_sensor_readings_status_color ON sensor_readings(status_color);
CREATE INDEX IF NOT EXISTS idx_plant_images_created_at ON plant_images(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_plant_metrics_created_at ON plant_metrics(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE sensor_readings ENABLE ROW LEVEL SECURITY;
ALTER TABLE plant_images ENABLE ROW LEVEL SECURITY;
ALTER TABLE plant_metrics ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (adjust as needed for your security requirements)
CREATE POLICY "Allow public read access to sensor_readings" ON sensor_readings FOR SELECT USING (true);
CREATE POLICY "Allow public insert access to sensor_readings" ON sensor_readings FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public read access to plant_images" ON plant_images FOR SELECT USING (true);
CREATE POLICY "Allow public insert access to plant_images" ON plant_images FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public delete access to plant_images" ON plant_images FOR DELETE USING (true);

CREATE POLICY "Allow public read access to plant_metrics" ON plant_metrics FOR SELECT USING (true);
CREATE POLICY "Allow public insert access to plant_metrics" ON plant_metrics FOR INSERT WITH CHECK (true);

-- Create storage bucket for plant images
INSERT INTO storage.buckets (id, name, public) 
VALUES ('plant-images', 'plant-images', true)
ON CONFLICT (id) DO NOTHING;

-- Create storage policies
CREATE POLICY "Allow public uploads to plant-images bucket" ON storage.objects 
FOR INSERT WITH CHECK (bucket_id = 'plant-images');

CREATE POLICY "Allow public downloads from plant-images bucket" ON storage.objects 
FOR SELECT USING (bucket_id = 'plant-images');

CREATE POLICY "Allow public deletes from plant-images bucket" ON storage.objects 
FOR DELETE USING (bucket_id = 'plant-images');

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update updated_at
CREATE TRIGGER update_sensor_readings_updated_at BEFORE UPDATE ON sensor_readings 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_plant_images_updated_at BEFORE UPDATE ON plant_images 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_plant_metrics_updated_at BEFORE UPDATE ON plant_metrics 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
