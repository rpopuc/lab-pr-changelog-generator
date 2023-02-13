<?php

namespace App\Domain\Entities;

class User
{
    private string $documentId;
    private string $name;
    private int $age;

    public function __construct(string $documentId, string $name, int $age)
    {
        $this->documentId = $documentId;
        $this->name = $name;
        $this->age = $age;
    }

    public function getFiscalId(): string
    {
        return $this->fiscalId;
    }

    public function getName(): string
    {
        return $this->name;
    }

    public function getAge(): int
    {
        return $this->age;
    }
}