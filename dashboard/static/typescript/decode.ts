

import * as RLP from "rlp";
import base64url from "base64url";
import { convertToString } from "@multiformats/multiaddr/convert";

export type NodeId = string;
export type SequenceNumber = bigint;

export type ENRKey = string;
export type ENRValue = Uint8Array;

export class ENR extends Map<ENRKey, ENRValue> {

    private _nodeId?: NodeId;

    constructor(kvs: Record<ENRKey, ENRValue> = {}) {
        super(Object.entries(kvs));
    }

    static decodeFromValues(decoded: Buffer[]): ENR {
        if (!Array.isArray(decoded)) {
            throw new Error("Decoded ENR must be an array");
        }
        if (decoded.length % 2 !== 0) {
            throw new Error("Decoded ENR must have an even number of elements");
        }

        const [signature, seq] = decoded;
        if (!signature || Array.isArray(signature)) {
            throw new Error("Decoded ENR invalid signature: must be a byte array");
        }
        if (!seq || Array.isArray(seq)) {
            throw new Error("Decoded ENR invalid sequence number: must be a byte array");
        }

        const obj: Record<ENRKey, ENRValue> = {};
        const signed: Buffer[] = [seq];
        for (let i = 2; i < decoded.length; i += 2) {
            const k = decoded[i];
            const v = decoded[i + 1];
            obj[k.toString()] = Buffer.from(v);
            signed.push(k, v);
        }
        const enr = new ENR(obj);
        return enr;
    }

    static decode(encoded: Buffer): ENR {
        const decoded = RLP.decode(encoded) as unknown as Buffer[];
        return ENR.decodeFromValues(decoded);
    }

    static decodeTxt(encoded: string): ENR {
        if (!encoded.startsWith("enr:")) {
            throw new Error("string encoded ENR must start with 'enr:'");
        }
        return ENR.decode(base64url.toBuffer(encoded.slice(4)));
    }

    get ip(): string | undefined {
        const raw = this.get("ip");
        if (raw) {
            return convertToString("ip4", toNewUint8Array(raw)) as string;
        } else {
            return undefined;
        }
    }

    get udp(): number | undefined {
        const raw = this.get("udp");
        if (raw) {
            return Number(convertToString("udp", toNewUint8Array(raw)));
        } else {
            return undefined;
        }
    }

    get client(): string | undefined {
        const shorthand = this.get("c");
        if (shorthand) {
            switch (shorthand[0]) {
                // ASCII 't'
                case 0x74:
                    return 'trin';
                // ASCII 'u'
                case 0x75:
                    return 'ultralight';
                // ASCII 'f'
                case 0x66:
                    return 'fluffy';
                default:
                    return undefined;
            }
        }
    }
}

function toNewUint8Array(buf: Uint8Array): Uint8Array {
    const arrayBuffer = buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength);
    return new Uint8Array(arrayBuffer);
}
