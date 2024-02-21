import Image from "next/image";
import Link from 'next/link';


export default function ImageList() {
    let category = ["classify", "detect", "pose", "segment"]
    return (
        <div>
            {
                category.map((a, i)=>{
                    return (
                        <div className="category" key={i}>
                            <Link href={"/" + a}>
                                <Image
                                    src={"/" + a + ".png"}
                                    alt={a + ".png"}
                                    className="dark"
                                    width={368}
                                    height={482}
                                    priority
                                />
                            </Link>
                        </div>
                    )
                })
            }
        </div>
  );
}