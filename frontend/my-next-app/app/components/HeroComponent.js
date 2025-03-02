import Image from "next/image";

export default function HeroComponent() {
    return (
        <div>
            <Image src="/hero.jpg" alt="Hero Image" width={700} height={700} />
        </div>
    );
}