import * as fs from 'fs';
import * as path from 'path';
import { Logger } from './translation-core';

// File operation utilities
export function ensureDirectoryExists(dirPath: string): void {
    if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
    }
}

export function readFileSafe(filePath: string): string | null {
    try {
        return fs.readFileSync(filePath, 'utf-8');
    } catch (error) {
        Logger.error(`Error reading file ${filePath}`, error);
        return null;
    }
}

export function writeFileSafe(filePath: string, content: string): boolean {
    try {
        ensureDirectoryExists(path.dirname(filePath));
        fs.writeFileSync(filePath, content, 'utf-8');
        return true;
    } catch (error) {
        Logger.error(`Error writing file ${filePath}`, error);
        return false;
    }
}

export function fileExists(filePath: string): boolean {
    return fs.existsSync(filePath);
}

export function deleteFileSafe(filePath: string): boolean {
    try {
        if (fs.existsSync(filePath)) {
            fs.unlinkSync(filePath);
            return true;
        }
        return false;
    } catch (error) {
        Logger.error(`Error deleting file ${filePath}`, error);
        return false;
    }
}

export function getFilesInDirectory(dirPath: string, pattern?: RegExp): string[] {
    try {
        if (!fs.existsSync(dirPath)) {
            return [];
        }
        
        const files = fs.readdirSync(dirPath);
        if (pattern) {
            return files.filter(file => pattern.test(file));
        }
        return files;
    } catch (error) {
        Logger.error(`Error reading directory ${dirPath}`, error);
        return [];
    }
}

export function copyFileSafe(sourcePath: string, destPath: string): boolean {
    try {
        ensureDirectoryExists(path.dirname(destPath));
        fs.copyFileSync(sourcePath, destPath);
        return true;
    } catch (error) {
        Logger.error(`Error copying file from ${sourcePath} to ${destPath}`, error);
        return false;
    }
}

export function getFileSize(filePath: string): number {
    try {
        const stats = fs.statSync(filePath);
        return stats.size;
    } catch (error) {
        Logger.error(`Error getting file size for ${filePath}`, error);
        return 0;
    }
}

export function isDirectory(path: string): boolean {
    try {
        return fs.statSync(path).isDirectory();
    } catch (error) {
        return false;
    }
}

export function createBackupFile(filePath: string): boolean {
    if (!fileExists(filePath)) {
        return false;
    }
    
    const backupPath = `${filePath}.backup`;
    return copyFileSafe(filePath, backupPath);
}

export function restoreBackupFile(filePath: string): boolean {
    const backupPath = `${filePath}.backup`;
    if (!fileExists(backupPath)) {
        return false;
    }
    
    return copyFileSafe(backupPath, filePath);
}