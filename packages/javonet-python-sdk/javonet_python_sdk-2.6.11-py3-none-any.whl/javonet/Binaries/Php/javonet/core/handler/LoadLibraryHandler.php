<?php

declare(strict_types=1);

namespace core\handler;

use Exception;
use ParseError;
use Phar;
use RecursiveDirectoryIterator;
use RecursiveIteratorIterator;
use utils\CommandInterface;
use utils\exception\JavonetArgumentsMismatchException;

final class LoadLibraryHandler extends AbstractHandler
{
    private const REQUIRED_ARGUMENTS_COUNT = 1;
    private const MAX_DIRECTORY_DEPTH = 10;
    private static array $loadedLibraries = [];
    private static array $loadedAutoloaders = [];
    private static array $registeredPsr4Autoloaders = [];
    private array $loadedClassPaths = [];

    public function process(CommandInterface $command): int
    {
        return $this->loadLibrary($command);
    }

    private function loadLibrary(CommandInterface $command): int
    {
        if ($command->getPayloadSize() < self::REQUIRED_ARGUMENTS_COUNT) {
            throw new JavonetArgumentsMismatchException(
                self::class,
                self::REQUIRED_ARGUMENTS_COUNT
            );
        }

        $assemblyName = (string) $command->getPayload()[0];

        if (!file_exists($assemblyName)) {
            throw new Exception('File not found: ' . $assemblyName);
        }

        // Normalize path first
        $canonicalPath = realpath($assemblyName);
        if ($canonicalPath === false) {
            throw new Exception('Cannot resolve path: ' . $assemblyName);
        }

        // Already loaded? bail out early
        if (in_array($canonicalPath, self::$loadedLibraries, true)) {
            return 0;
        }

        // Use canonical path for type detection as well
        if (is_dir($canonicalPath)) {
            $this->loadDirectory($canonicalPath);
        } elseif (pathinfo($canonicalPath, PATHINFO_EXTENSION) === 'phar') {
            $this->loadPharFile($canonicalPath);
        } else {
            $this->loadPhpFile($canonicalPath);
        }

        self::$loadedLibraries[] = $canonicalPath;
        return 0;
    }

    private function loadDirectory(string $directoryPath): void
    {
        if (!is_readable($directoryPath)) {
            throw new Exception('Directory is not readable: ' . $directoryPath);
        }

        $realPath = realpath($directoryPath);
        if ($realPath === false) {
            throw new Exception('Cannot resolve directory path: ' . $directoryPath);
        }

        $currentIncludePath = get_include_path();
        if (strpos($currentIncludePath, $realPath) === false) {
            set_include_path($currentIncludePath . PATH_SEPARATOR . $realPath);
            $this->loadedClassPaths[] = $realPath;
        }

        $this->autoloadPhpFilesFromDirectory($realPath);
    }

    private function loadPharFile(string $pharPath): void
    {
        if (!is_readable($pharPath)) {
            throw new Exception('PHAR file is not readable: ' . $pharPath);
        }

        $realPath = realpath($pharPath);
        if ($realPath === false) {
            throw new Exception('Cannot resolve PHAR path: ' . $pharPath);
        }

        try {
            $phar = new Phar($realPath);

            $currentIncludePath = get_include_path();
            if (strpos($currentIncludePath, $realPath) === false) {
                set_include_path($currentIncludePath . PATH_SEPARATOR . $realPath);
                $this->loadedClassPaths[] = $realPath;
            }

            if (isset($phar['bootstrap.php'])) {
                include_once 'phar://' . $realPath . '/bootstrap.php';
            }
        } catch (Exception $e) {
            throw new Exception(sprintf('Error loading PHAR file %s : %s', $pharPath, $e->getMessage()));
        }
    }

    private static array $loadedPhpFiles = []; // optional extra safeguard

    private function loadPhpFile(string $filePath): void
    {
        if (!is_readable($filePath)) {
            throw new Exception('PHP file is not readable: ' . $filePath);
        }

        $realPath = realpath($filePath);
        if ($realPath === false) {
            throw new Exception('Cannot resolve PHP file path: ' . $filePath);
        }

        $fileExtension = pathinfo($realPath, PATHINFO_EXTENSION);
        if (!in_array($fileExtension, ['php', 'inc'], true)) {
            throw new Exception('File is not a valid PHP file: ' . $realPath);
        }

        // OPTIONAL: skip if we already loaded this exact file
        if (in_array($realPath, self::$loadedPhpFiles, true)) {
            return;
        }

        $code = file_get_contents($realPath);
        if ($code === false) {
            throw new Exception(sprintf('Failed to read php file: %s', $realPath));
        }

        try {
            token_get_all($code, TOKEN_PARSE);
        } catch (ParseError $e) {
            throw new Exception(sprintf('PHP syntax error in file %s: %s', $realPath, $e->getMessage()));
        }

        $lastError = error_get_last();
        if ($lastError && $lastError['type'] === E_PARSE) {
            throw new Exception(sprintf('PHP syntax error in file %s: %s', $realPath, $lastError['message']));
        }

        // Try to find and load Composer autoloader before including the file
        $this->findAndLoadComposerAutoloader($realPath);

        include_once $realPath;
        self::$loadedPhpFiles[] = $realPath;
    }

    /**
     * Searches for Composer autoloader in the directory hierarchy and loads it.
     * Falls back to registering PSR-4 autoloader from composer.json if vendor/autoload.php is not available.
     */
    private function findAndLoadComposerAutoloader(string $filePath): void
    {
        $directory = dirname($filePath);

        for ($i = 0; $i < self::MAX_DIRECTORY_DEPTH; $i++) {
            $vendorAutoloader = $directory . DIRECTORY_SEPARATOR . 'vendor' . DIRECTORY_SEPARATOR . 'autoload.php';
            $composerJson = $directory . DIRECTORY_SEPARATOR . 'composer.json';

            // Prefer ready-made vendor autoloader
            if (file_exists($vendorAutoloader)) {
                $this->loadVendorAutoloader($vendorAutoloader);
                return;
            }

            // Fallback: build autoloader from composer.json
            if (file_exists($composerJson)) {
                $this->registerAutoloaderFromComposerJson($composerJson, $directory);
                return;
            }

            $parentDirectory = dirname($directory);
            // Reached filesystem root
            if ($parentDirectory === $directory) {
                break;
            }
            $directory = $parentDirectory;
        }
    }

    /**
     * Loads vendor autoloader if not already loaded.
     */
    private function loadVendorAutoloader(string $autoloaderPath): void
    {
        $realAutoloaderPath = realpath($autoloaderPath);

        if ($realAutoloaderPath === false) {
            return;
        }

        // Don't load the same autoloader twice
        if (in_array($realAutoloaderPath, self::$loadedAutoloaders, true)) {
            return;
        }

        include_once $realAutoloaderPath;
        self::$loadedAutoloaders[] = $realAutoloaderPath;
    }

    /**
     * Registers PSR-4 autoloader based on composer.json configuration.
     * This is a fallback when vendor/autoload.php is not available.
     */
    private function registerAutoloaderFromComposerJson(string $composerJsonPath, string $baseDir): void
    {
        $realComposerJsonPath = realpath($composerJsonPath);

        if ($realComposerJsonPath === false) {
            return;
        }

        // Don't register autoloader for the same composer.json twice
        if (in_array($realComposerJsonPath, self::$registeredPsr4Autoloaders, true)) {
            return;
        }

        $composerContent = file_get_contents($realComposerJsonPath);
        if ($composerContent === false) {
            return;
        }

        $composerConfig = json_decode($composerContent, true);
        if ($composerConfig === null || !isset($composerConfig['autoload']['psr-4'])) {
            return;
        }

        $psr4Map = $composerConfig['autoload']['psr-4'];
        $realBaseDir = realpath($baseDir) ?: $baseDir;

        spl_autoload_register(function (string $class) use ($psr4Map, $realBaseDir): void {
            foreach ($psr4Map as $prefix => $path) {
                $prefixLength = strlen($prefix);

                if (strncmp($class, $prefix, $prefixLength) !== 0) {
                    continue;
                }

                $relativeClass = substr($class, $prefixLength);
                $file = $realBaseDir . DIRECTORY_SEPARATOR . $path . str_replace('\\', DIRECTORY_SEPARATOR, $relativeClass) . '.php';

                if (file_exists($file)) {
                    include_once $file;
                    return;
                }
            }
        });

        self::$registeredPsr4Autoloaders[] = $realComposerJsonPath;
    }

    private function autoloadPhpFilesFromDirectory(string $directory): void
    {
        $iterator = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($directory)
        );

        foreach ($iterator as $file) {
            if ($file->isFile() && $file->getExtension() === 'php') {
                $realPath = $file->getRealPath() ?: $file->getPathname();

                // Optional: same guard as loadPhpFile
                if (in_array($realPath, self::$loadedPhpFiles, true)) {
                    continue;
                }

                include_once $realPath;
                self::$loadedPhpFiles[] = $realPath;
            }
        }
    }

    public static function getLoadedLibraries(): array
    {
        return self::$loadedLibraries;
    }

    public function __destruct()
    {
        foreach ($this->loadedClassPaths as $path) {
            if (strpos($path, sys_get_temp_dir()) === 0 && is_dir($path)) {
                $this->removeDirectoryOrFile($path);
            }
        }
    }

    private function removeDirectoryOrFile(string $dir): void
    {
        if (!file_exists($dir)) {
            return;
        }

        if (is_file($dir) || is_link($dir)) {
            if (!unlink($dir)) {
                throw new Exception('Cannot delete file path: ' . $dir);
            }

            return;
        }
        $files = scandir($dir);
        foreach ($files as $file) {
            if ($file === '.' || $file === '..') {
                continue;
            }
            $this->removeDirectoryOrFile($dir . DIRECTORY_SEPARATOR . $file);
        }

        if(!rmdir($dir)) {
            throw new Exception('Cannot delete dir path: '. $dir);
        }
    }
}
