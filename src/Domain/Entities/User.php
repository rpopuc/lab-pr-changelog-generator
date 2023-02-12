<?php

namespace App\Domain\Entities;

class User
{
    private string $fiscalId;
    private string $name;
    private int $age;

    public function __construct(string $fiscalId, string $name, int $age)
    {
        $this->fiscalId = $fiscalId;
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